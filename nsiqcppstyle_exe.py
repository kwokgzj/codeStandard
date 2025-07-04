#!/usr/bin/env python
#
# Copyright (c) 2009 NHN Inc. All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#    * Neither the name of NHN Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import copy
import functools
import re
import sys
import tempfile
from dataclasses import dataclass
from enum import Flag, auto
from pathlib import Path
from typing import List, Set

import nsiqcppstyle_checker
import nsiqcppstyle_reporter
import nsiqcppstyle_rulemanager
import nsiqcppstyle_state
from __about__ import __version__ as version
from nsiqcppstyle_outputer import _consoleOutputer as console
from nsiqcppstyle_util import *

##########################################################################
title = "nsiqcppstyle: N'SIQ Cpp Style ver " + version + "\n"


def ShowMessageAndExit(msg, usageOutput=True):
    console.Err.Error(msg)
    if usageOutput:
        get_parser().print_usage()
        sys.exit(0)
    sys.exit(-1)


def get_parser():
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=title
        + """Apply custom rules on C/C++ code to report violations of your coding standards

[Example]
   nsiqcppstyle .
   nsiqcppstyle targetdir
   nsiqcppstyle -f filefilterpath targetfilepath
""",
        epilog="""

* If options like `--filter-string` and `--var` (which accept one or more arguments) are the last option, remember to separate the arguments and targets by adding a `--` before the targets. Eg:
  --var key1:value key2:value -- my_target_path

* By default, it doesn't apply any rules on the source. If you want to apply rule, they should be provided in the 'filefilter.txt' file with the following format:
  ~ RULENAME

* You can  customize the rule behavior by insert key-value pairs in the 'filefilter.txt' with the following format:
  % key: value

* If you want to filter in or out some source code files in the target directory please locate 'filefilter.txt' file in the target directory in the form of

  * FILTER_SCOPE_NAME
  + INCLUDE_PATH_PATTERNS
  - EXCLUDE_PATH_PATTERNS
  = LANGUAGE_NAME: EXTENSION,LANGUAGE_NAME: EXTENSION

  The filter scope name is the identifier to selectively apply filter. In case of the quality, Maybe only main sources except test should be measured. Otherwise, to measure the productivity, the test code might be measured as well. To keep this information in the same file('filefilter.txt'), you can provide the '* file_scope_name' before the filter configuration starts.
  You can define multiple filter scope names in the 'filefilter.txt'. We recommend you define at least two filter scopes (Productivity, Quality)

  The included(+)/excluded(-) paths are applied sequentially from top to bottom
  By default, all files under target directory are included for analysis excluding the version control (cvs, svn, git, mercurial) directories.

* If the 'basefilelist.txt' (pair of filename and filesize) is in the target directory, nsiqcppstyle recognizes it and checks only the new and modified file
""",
    )

    verbosity_gp = parser.add_mutually_exclusive_group(required=False)
    verbosity_gp.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Show detail output (verbose mode)",
    )
    verbosity_gp.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Enable quiet mode. If enabled, this tool only reports errors.",
    )
    verbosity_gp.add_argument(
        "--ci",
        action="store_true",
        default=False,
        help="Enable Continuous Integration mode. If enabled, this tool only reports summary.",
    )
    verbosity_gp.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error"],
        default="info",
        help="Set a logging level",
    )

    parser.add_argument("--version", action="version", version="%(prog)s " + version)
    parser.add_argument("--show-url", action="store_true", default=False)
    parser.add_argument("-r", "--list-rules", action="store_true", default=False, help="Show rule list")
    parser.add_argument(
        "--var",
        action="extend",
        nargs="+",
        help="Provide variables in 'KEY:VALUE' format to customize the rule behavior. Can be used multiple times",
    )
    parser.add_argument(
        "--output",
        choices=[
            "csv",
            "eclipse",
            "emacs",
            "vs7",
            "xml",
        ],
        default="vs7",
        help="'emacs', 'vs7', 'eclipse' output the result on the stdout in the form that each tool recognizes. 'csv' and 'xml' output the result on the file 'nsiqcppstyle_result.<extension>' if you don't provide -o option",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        default="",
        help="Output location, required for multiple targets. If a file is provided, the parent folder is used instead",
    )
    parser.add_argument(
        "-s",
        "--filter-scope",
        default="default",
        help="Assign Filter scope name to be applied in this analysis",
    )

    filter_gp = parser.add_mutually_exclusive_group(required=False)
    filter_gp.add_argument(
        "-f",
        "--filter-path",
        default="",
        help="Custom location of 'filefilter.txt'. By default the directory of the target is searched for  the 'filefilter.txt'",
    )

    filter_gp.add_argument(
        "--filter-string",
        action="extend",
        nargs="+",
        help="A single, valid filter file line. Enables specifying the contents of a filter file without creating one (e.g., in a read-only file system). Can be used multiple times",
    )

    parser.add_argument(
        "--noBase",
        action="store_false",
        help="Use an null base file list instead of creating one from target",
    )
    parser.add_argument("target_path", nargs="+")
    return parser


@functools.lru_cache
def is_fs_case_sensitive(path: Path):
    dir = path.parent if path.is_file() else path
    with tempfile.NamedTemporaryFile(prefix="TmP", dir=dir, delete=True) as tmp_file:
        return not os.path.exists(tmp_file.name.lower())


def check_file_ext(filename: Path, valid_extensions: List[str]):
    """check if extension of filename is in valid_extensions"""
    if not filename.is_file():
        return False
    suffix = filename.suffix[1:]
    sufix = suffix if is_fs_case_sensitive(filename.parent) else suffix.lower()
    return suffix in valid_extensions


def main():
    global filename

    parser = get_parser()
    args = parser.parse_args()
    _nsiqcppstyle_state.output_format = args.output
    _nsiqcppstyle_state.showUrl = args.show_url
    filterScope = args.filter_scope
    targetPaths = GetRealTargetPaths(args.target_path)
    outputPath = args.output_path
    filterPath = args.filter_path
    filterStringList = args.filter_string
    noBase = args.noBase
    varMap = GetCliKeyValueMap(args.var)

    if args.verbose:
        console.SetLevel(console.Level.Verbose)
    elif args.quiet:
        console.SetLevel(console.Level.Error)
    elif args.ci:
        console.SetLevel(console.Level.Ci)
    else:
        import logging

        console.SetLevel(getattr(logging, str(args.log_level).upper()))

    if args.list_rules:
        ShowRuleList()
    try:
        extLangMap = {
            "Html": {"htm", "html"},
            "Java": {"java"},
            "Javascript/ActionScript": {"js", "as"},
            "JSP/PHP": {"jsp", "php", "JSP", "PHP"},
            "C/C++": {"cpp", "h", "c", "hxx", "cxx", "hpp", "cc", "hh", "m", "mm"},
        }

        # console.Out.Ci(title)
        runtimePath = GetRuntimePath()
        sys.path.append(runtimePath)

        multipleTarget = len(targetPaths) > 1

        # If multiple target
        if multipleTarget:
            if len(outputPath) == 0:
                ShowMessageAndExit("OutputPath(-o) should be provided to analyze multiple targets")
        else:
            outputPath = GetOutputPath(targetPaths[0], outputPath)
        ruleManager = nsiqcppstyle_rulemanager.ruleManager

        cExtendstionSet = extLangMap.get("C/C++")

        nsiqcppstyle_reporter.PrepareReport(outputPath, _nsiqcppstyle_state.output_format)
        analyzedFiles = []
        filter = None

        for targetPath in targetPaths:
            nsiqcppstyle_reporter.StartTarget(targetPath)
            extLangMapCopy = copy.deepcopy(extLangMap)
            targetName = targetPath.name
            # console.Out.Ci(console.Separator)
            # console.Out.Ci(f"=  Analyzing {targetName} ")

            if filterPath != "":
                filefilterPath = filterPath
            elif targetPath.is_file():
                filefilterPath = targetPath.parent / "filefilter.txt"
            else:
                filefilterPath = targetPath / "filefilter.txt"
            basefilelist = NullBaseFileList() if noBase else BaseFileList(targetPath)

            # Get Active Filter
            filterManager = FilterManager(str(filefilterPath), filterStringList, extLangMapCopy, varMap, filterScope)

            if filterScope != filterManager.GetActiveFilter().filterName:
                console.Out.Error(
                    f"\n{filterScope} filter scope is not available. Instead, use {filterManager.GetActiveFilter().filterName}\n",
                )

            filter = filterManager.GetActiveFilter()
            # Load Rule

            if len(filter.nsiqCppStyleRules) == 0:
                ShowMessageAndExit(f"Error!. Rules must be set in {filefilterPath}", False)
                continue

            ruleManager.LoadRules(filter.nsiqCppStyleRules)
            ruleManager.RunSessionStartRules()

            _nsiqcppstyle_state.checkers = filter.nsiqCppStyleRules
            _nsiqcppstyle_state.varMap = filter.varMap
            nsiqcppstyle_reporter.ReportRules(ruleManager.availRuleNames, filter.nsiqCppStyleRules)

            # console.Out.Info(filter.to_string())
            # console.Out.Ci(console.Separator)
            # console.Out.Verbose(f"* run nsiqcppstyle analysis on {targetName}")

            # if the target is file, analyze it without condition
            if targetPath.is_file():
                if check_file_ext(targetPath, cExtendstionSet):
                    ProcessFile(ruleManager, targetPath, analyzedFiles)

            # if the target is directory, analyze it with filefilter and
            # basefilelist
            else:
                for root, dirs, files in os.walk(targetPath):
                    if ".cvs" in dirs:
                        dirs.remove(".cvs")
                    if ".svn" in dirs:
                        dirs.remove(".svn")
                    if ".git" in dirs:
                        dirs.remove(".git")
                    if ".hg" in dirs:
                        dirs.remove(".hg")
                    for fname in files:
                        eachFile = os.path.join(root, fname)
                        basePart = eachFile[len(targetPath) :]
                        if (
                            check_file_ext(Path(fname), cExtendstionSet)
                            and basefilelist.IsNewOrChanged(eachFile)
                            and filter.CheckFileInclusion(basePart)
                        ):
                            nsiqcppstyle_reporter.StartFile(os.path.dirname(basePart), fname)
                            ProcessFile(ruleManager, eachFile, analyzedFiles)
                            nsiqcppstyle_reporter.EndFile()
            ruleManager.RunProjectRules(targetPath)
            nsiqcppstyle_reporter.EndTarget()

        # nsiqcppstyle_reporter.ReportSummaryToScreen(analyzedFiles, _nsiqcppstyle_state, filter)
        nsiqcppstyle_reporter.CloseReport(_nsiqcppstyle_state.output_format)
        ruleManager.RunSessionEndRules()
        return _nsiqcppstyle_state.error_count

    except Exception as err:
        console.Err.Error(err)
        console.Err.Error("for help use --help")
        sys.exit(-1)


# 3


def ProcessFile(ruleManager, file, analyzedFiles):
    # console.Out.Info("Processing: ", file)
    nsiqcppstyle_checker.ProcessFile(ruleManager, file)
    analyzedFiles.append(file)


def GetOutputPath(outputBasePath, outputPath):
    "Returns the LOC and complexity result path"
    if outputPath == "":
        outputPath = os.path.dirname(outputBasePath) if os.path.isfile(outputBasePath) else outputBasePath
    return os.path.realpath(outputPath)


def GetRealTargetPaths(args):
    """extract real target path list from args"""
    if len(args) == 0:
        ShowMessageAndExit("Error!: Target directory must be provided")
    targetPaths: List[Path] = []
    for eachTarget in args:
        realPath = Path(os.path.realpath(eachTarget))
        targetPaths.append(realPath)
        #       CheckPathPermission(realPath, "Target directory")
        if not realPath.exists():
            ShowMessageAndExit(f"Error!: Target directory {eachTarget} does not exist")
    return targetPaths


##########################################################################

##############################################################################
# Filter Manager
# - Load Filter
##############################################################################


class FilterManager:
    defaultFilterName = "default"
    singleQuote = "'"
    doubleQuote = '"'

    def _ProcessFilterLine(self, filter, raw_line):
        # <raw_line> may be enclosed in single/double quotes, and
        # the inner string may start/end with whitespace, clean it
        # up before using it.
        line = RemoveOuterQuotes(raw_line)

        if line.startswith("#") or len(line) == 0:
            # Comment or empty line, just return
            return filter
        if line.startswith("*"):
            if len(line[1:].strip()) != 0:
                filterName = line[1:].strip()
                filter = self.GetFilter(filterName)
        elif line.startswith("="):
            if len(line[1:].strip()) != 0:
                filter.AddLangMap(line[1:].strip(), '"' + line + '" of filefilter.txt')
        elif line.startswith("~"):
            if len(line[1:].strip()) != 0:
                filter.AddCppChecker(line[1:].strip())
        elif line.startswith("+"):
            arg = line[1:].strip()
            if arg != "":
                filter.AddInclude(arg)
        elif line.startswith("-"):
            arg = line[1:].strip()
            if arg != "":
                filter.AddExclude(arg)
        elif line.startswith("%"):
            arg = line[1:].strip()
            if arg != "":
                filter.AddVarMap(arg, '"' + arg + '" of filefilter.txt')

        return filter

    def __init__(self, fileFilterPath, filterStringList, extLangMap, varMap, activeFilterName):
        self.fileFilterPath = fileFilterPath
        self.baseExtLangMap = extLangMap
        self.baseVarMap = varMap
        self.filterMap = {FilterManager.defaultFilterName: self.CreateNewFilter(FilterManager.defaultFilterName)}
        filter = self.GetFilter(self.defaultFilterName)
        self.activeFilterName = self.defaultFilterName

        if filterStringList:
            for line in filterStringList:
                filter = self._ProcessFilterLine(filter, line)

        f = self.GetFilterFile(fileFilterPath)
        if f:
            for line in f.readlines():
                filter = self._ProcessFilterLine(filter, line)
            f.close()

        if len(filter.nsiqCppStyleRules) == 0:
            filter.AddExclude("/.svn/")
            filter.AddExclude("/.cvs/")
            filter.AddExclude("/.git/")
            return

        for eachMapKey in self.filterMap:
            self.filterMap[eachMapKey].AddExclude("/.cvs/")
            self.filterMap[eachMapKey].AddExclude("/.svn/")
            self.filterMap[eachMapKey].AddExclude("/.git/")

        if activeFilterName in self.filterMap:
            self.activeFilterName = activeFilterName

    def CreateNewFilter(self, filterName):
        return Filter(filterName, copy.deepcopy(self.baseExtLangMap), copy.deepcopy(self.baseVarMap))

    def GetFilter(self, filterName):
        if filterName not in self.filterMap:
            self.filterMap[filterName] = self.CreateNewFilter(filterName)
        return self.filterMap[filterName]

    def GetActiveFilter(self):
        return self.GetFilter(self.activeFilterName)

    def GetFilterFile(self, filterfile):
        if not os.path.exists(filterfile):
            return None
        return open(filterfile)


##############################################################################
# Filter
# - Represent each Filter
# - Check if the file is included or not
##############################################################################
def recursive_star_replace(string):
    recursive_star = re.compile(rf"(.*)\*\*{os.sep}(.*)")  # search for **/
    split = recursive_star.split(string)
    if len(split) != 1:
        _empty, remainder, post_star, _empty2 = split
        top_level = remainder == ""
        if not (top_level or remainder.endswith(os.sep)):
            msg = f"Except the beginning, the pattern (**) must be sandwitched between directory separator ({os.sep})"
            raise ValueError(msg)
        post_star = post_star.removeprefix(os.sep)  # ** = recursive, including no subdirectories
        pre_star = recursive_star_replace(remainder) if not top_level else ""
        string = rf"{pre_star}(.+{os.sep})?{post_star}"
    return string


def single_star_replace(string):
    single_star = re.compile(r"([^*]+)\*([^*]+)")
    split = single_star.split(string)
    if len(split) != 1:
        start, pre_star, post_star, remainder = split
        post_star_full = single_star_replace(post_star + remainder) if remainder != "" else post_star
        string = rf"{start}{pre_star}[^{os.sep}]*{post_star_full}"
    return string


def generate_regex(string):
    string = string.replace(".", "\\.")  # escape extension
    single_star_start = re.compile(r"^\*([^*].*)")
    string = single_star_replace(string)
    if match_item := single_star_start.match(string):
        string = rf"[^{os.sep}]*".join([""] + list(match_item.groups()))
    return recursive_star_replace(string)


class FileFilter:
    def __init__(self, filter_string: str, include: bool = True):
        self.include = include
        self.filter_string = filter_string

        if "*" not in self.filter_string:
            # prefix search capability only
            regex = rf"^{re.escape(filter_string)}"
        else:
            console.Out.Info(
                "Found '*', using new pattern matching method. Please use Python 3.13 if you have * in your filename",
            )
            if sys.version_info >= (3, 13):
                from glob import translate  # type: ignore[attr-defined] # sys version already checked

                regex = translate(self.filter_string, recursive=True, include_hidden=True)
            else:
                # use custom technique, might have bugs
                regex = generate_regex(self.filter_string)
        self.filter_regex: re.Pattern = re.compile(regex)

    def __hash__(self):
        return hash(self.filter_string)

    def __eq__(self, other):
        if not isinstance(other, FileFilter):
            return False
        return self.filter_string == other.filter_string

    def __repr__(self):
        status = "included" if self.include else "excluded"
        return f"{self.filter_string} is {status}"


class Filter:
    """
    Filter
    - Represent each Filter
    - Check if the file is included or not
    """

    def __init__(self, filterName, baseExtLangMap, baseVarMap):
        self.extLangMap = baseExtLangMap
        self.varMap = baseVarMap
        self.filterName = filterName
        self.filefilter: List[FileFilter] = []
        self.match = re.compile("^(\\\\|//)")
        self.nsiqCppStyleRules = []

    def to_string(self):
        template = """Filter Scope "%s" is applied.
Current Filter Setting (Following is applied sequentially)
%s
Current File extension and Language Settings
%s"""
        s = ""
        for count, eachfilter in enumerate(self.filefilter):
            s = s + (f"  {count+1}. {eachfilter}\n")
        return template % (self.filterName, s, self.GetLangString())

    def __repr__(self):
        return self.to_string()

    def NormalizePath(self, filter_string):
        replacedpath = filter_string.replace("/", os.path.sep)
        replacedpath = replacedpath.replace("\\\\", os.path.sep)
        return replacedpath.replace("\\", os.path.sep)

    def AddInclude(self, filter_string):
        self.AddFilter(True, filter_string)

    def AddExclude(self, filter_string):
        self.AddFilter(False, filter_string)

    def AddCppChecker(self, eachChecker):
        self.nsiqCppStyleRules.append(eachChecker)

    def AddFilter(self, inclusion, filter_string):
        if filter_string.startswith(("\\\\", "//")):
            filter_string = self.match.sub("", filter_string)

        filterString = self.NormalizePath(filter_string)
        if filter_string in self.filefilter:
            self.filefilter.remove(FileFilter(filter_string=filterString))
        self.filefilter.append(FileFilter(filterString, inclusion))

    def GetFileFilter(self):
        return self.filefilter

    def GetLangString(self):
        s = ""
        for eachKey in self.extLangMap:
            if eachKey == "C/C++":
                s = s + "  " + eachKey + "="
                extSet = self.extLangMap.get(eachKey)
                setLen = len(extSet)
                count = 0
                for eachExt in extSet:
                    count = count + 1
                    s = s + eachExt
                    s = s + "," if count < setLen else s + "\n"
        return s

    def CheckFileInclusion(self, fileStr):
        filename = self.NormalizePath(fileStr)
        inclusion = True
        for eachfilter in self.filefilter:
            if eachfilter.filter_regex.match(filename) is None:
                continue
            inclusion = eachfilter.include
        return inclusion

    def GetLangMap(self):
        return self.extLangMap

    def AddLangMap(self, langMapString, where):
        langExtList = langMapString.split(",")
        for eachExt in langExtList:
            extLangPair = eachExt.split(": ")
            if len(extLangPair) != 2:
                ShowMessageAndExit(
                    f"Error!: The extension and language pair ({langMapString}) is incorrect in {where}, please use LANGUAGENAME: EXTENSION style",
                )
            lang, ext = extLangPair
            self.extLangMap.get(lang).add(ext)

    def AddVarMap(self, keyValuePairString, where):
        varMap = GetCustomKeyValueMap(keyValuePairString, where)
        for eachVar in varMap:
            if eachVar in self.varMap:
                continue
            self.varMap[eachVar] = varMap[eachVar]


def GetCliKeyValueMap(kvList):
    if kvList is None:
        return {}

    varMap = {}
    for kv in kvList:
        kvPair = kv.split(":", 1)
        if len(kvPair) != 2:
            ShowMessageAndExit(
                f"Error!: No key found in {kv}. Please use KEY:VALUE style to provide key and value",
            )
        varMap[kvPair[0]] = kvPair[1]

    return varMap


def GetCustomKeyValueMap(keyValuePair, where):
    varMap = {}
    customKeyValues = keyValuePair.split(",")
    for eachCustomKeyValue in customKeyValues:
        customKeyValuePair = eachCustomKeyValue.split(": ")
        if len(customKeyValuePair) != 2:
            ShowMessageAndExit(
                f"Error!: The var key and value pair ({keyValuePair}) is incorrect in {where}, please use KEY: VALUE style",
            )
        key, value = customKeyValuePair
        varMap[key] = value
    return varMap


##############################################################################
# BaseFileList
##############################################################################


class BaseFileList:
    """
    - Represent  basefilelist.txt state
    - It check if the current file and size pair is in the basefilelist.
    """

    def __init__(self, targetDir):
        self.baseFileList = {}
        if os.path.isdir(targetDir):
            fsrc = os.path.join(targetDir, "basefilelist.txt")
            if os.path.exists(fsrc):
                with open(fsrc) as f:
                    for line in f.readlines():
                        self.baseFileList[line.strip()] = True

    def IsNewOrChanged(self, filename):
        item = os.path.basename(filename) + str(os.path.getsize(filename))
        return not self.baseFileList.get(item, False)


class NullBaseFileList:
    """
    - Represent  basefilelist.txt state
    - It check if the current file and size pair is in the basefilelist.
    """

    def __init__(self):
        pass

    def IsNewOrChanged(self, filename):
        return True


def ShowRuleList():
    nsiqcppstyle_rulemanager.ruleManager.availRuleNames.sort()
    for rule in nsiqcppstyle_rulemanager.ruleManager.availRuleNames:
        if rule.startswith("RULE_"):
            print("~", rule)
    sys.exit(1)


def CheckPathPermission(path, folderrole):
    if not os.access(path, os.R_OK) and os.path.exists(path):
        ShowMessageAndExit(f"Error!: {folderrole}  You should have read permission in {path}.")
    return True


##########################################################################


_nsiqcppstyle_state = nsiqcppstyle_state._nsiqcppstyle_state


if __name__ == "__main__":
    sys.path.append(GetRuntimePath())
    sys.exit(main())
