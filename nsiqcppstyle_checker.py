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
# ----------------------------------------------------------------------

import os
import traceback
from copy import deepcopy

from nsiqcppstyle_outputer import _consoleOutputer as console
from nsiqcppstyle_rulehelper import *  # @UnusedWildImport

import chardet

# Reserved words

tokens = [
    "ID",
    # Operators (+,-,*,/,%,|,&,~,^,<<,>>, ||, &&, !, <, <=, >, >=, ==, !=, <=>)
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MODULO",
    "OR",
    "AND",
    "NOT",
    "XOR",
    "LSHIFT",
    "RSHIFT",
    "LOR",
    "LAND",
    "LNOT",
    "LT",
    "LE",
    "GT",
    "GE",
    "EQ",
    "NE",
    "SPACESHIP",
    # Assignment (=, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |=)
    "EQUALS",
    "TIMESEQUAL",
    "DIVEQUAL",
    "MODEQUAL",
    "PLUSEQUAL",
    "MINUSEQUAL",
    "LSHIFTEQUAL",
    "RSHIFTEQUAL",
    "ANDEQUAL",
    "XOREQUAL",
    "OREQUAL",
    # Increment/decrement (++,--)
    "PLUSPLUS",
    "MINUSMINUS",
    # Structure dereference (->)
    "ARROW",
    # Ternary operator (?)
    "TERNARY",
    # Delimeters ( ) [ ] { } , . ; :
    "LPAREN",
    "RPAREN",
    "PARENS",
    "LBRACKET",
    "RBRACKET",
    "LBRACE",
    "RBRACE",
    "COMMA",
    "PERIOD",
    "SEMI",
    "COLON",
    "DOUBLECOLON",
    # Ellipsis (...)
    "ELLIPSIS",
    # macro
    "PREPROCESSOR",
    "SHARPSHARP",
    "SHARP",
    # non-macro
    "NUMBER",
    "CHARACTER",
    "STRING",
    "SPACE",
    "COMMENT",
    "CPPCOMMENT",
    "LINEFEED",
    "PREPROCESSORNEXT",
    "ASM",
    "IGNORE",
    "DEFAULT",
    "DELETE",
    # cast
    "CONST_CAST",
    "DYNAMIC_CAST",
    "REINTERPRET_CAST",
    "STATIC_CAST",
    # control
    "CONST",
    "WHILE",
    "IF",
    "FOR",
    "DO",
    "ELSE",
    "ENUM",
    "EXPORT",
    "EXTERN",
    "TRUE",
    "FALSE",
    "GOTO",
    "SWITCH",
    "CASE",
    "CONTST",
    "CATCH",
    "BREAK",
    "CONTINUE",
    "TRY",
    "THROW",
    # Operator
    "NEW",
    "OPERATOR",
    "SIZEOF",
    "INLINE",
    "NAMESPACE",
    "RETURN",
    # visibility
    "PUBLIC",
    "PRIVATE",
    "PROTECTED",
    # Type
    "STATIC",
    "STRUCT",
    "TEMPLATE",
    "THIS",
    "TYPEDEF",
    "TYPENAME",
    "UNION",
    "USING",
    "VIRTUAL",
    "CLASS",
    "AUTO",
    "CHAR",
    "INT",
    "LONG",
    "DOUBLE",
    "FLOAT",
    "SHORT",
    "BOOL",
    "VOID",
]

# Operators
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_MODULO = r"%"
t_OR = r"\|"
t_AND = r"&"
t_NOT = r"~"
t_XOR = r"\^"
t_LSHIFT = r"<<"
t_RSHIFT = r">>"
t_LOR = r"\|\|"
t_LAND = r"&&"
t_LNOT = r"!"
t_LT = r"<"
t_GT = r">"
t_LE = r"<="
t_GE = r">="
t_EQ = r"=="
t_NE = r"!="
t_SPACESHIP = r"<=>"
t_DOUBLECOLON = r"::"
# Assignment operators

t_PREPROCESSOR = r"\#\s*[A-Za-z_][A-Za-z0-9_]*"
t_EQUALS = r"="
t_TIMESEQUAL = r"\*="
t_DIVEQUAL = r"/="
t_MODEQUAL = r"%="
t_PLUSEQUAL = r"\+="
t_MINUSEQUAL = r"-="
t_LSHIFTEQUAL = r"<<="
t_RSHIFTEQUAL = r">>="
t_ANDEQUAL = r"&="
t_OREQUAL = r"\|="
t_XOREQUAL = r"\^="

# Increment/decrement
t_PLUSPLUS = r"\+\+"
t_MINUSMINUS = r"--"

# ->
t_ARROW = r"->"

# ?
t_TERNARY = r"\?"

# Delimiters
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_COMMA = r","
t_PERIOD = r"\."
t_SEMI = r";"
t_COLON = r":"
t_ELLIPSIS = r"\.\.\."


# Identifiers
def t_ID(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.type = reserved.get(t.value, "ID")
    return t


reserved = {
    "for": "FOR",
    "class": "CLASS",
    "asm": "ASM",
    "switch": "SWITCH",
    "case": "CASE",
    "catch": "CATCH",
    "auto": "AUTO",
    "break": "BREAK",
    "continue": "CONTINUE",
    "default": "DEFAULT",
    "delete": "DELETE",
    "const_cast": "CONST_CAST",
    "dynamic_cast": "DYNAMIC_CAST",
    "reinterpret_cast": "REINTERPRET_CAST",
    "static_cast": "STATIC_CAST",
    "while": "WHILE",
    "if": "IF",
    "do": "DO",
    "else": "ELSE",
    "enum": "ENUM",
    "export": "EXPORT",
    "extern": "EXTERN",
    "true": "TRUE",
    "false": "FALSE",
    "const": "CONST",
    "goto": "GOTO",
    "inline": "INLINE",
    "namespace": "NAMESPACE",
    "new": "NEW",
    "operator": "OPERATOR",
    "return": "RETURN",
    "public": "PUBLIC",
    "private": "PRIVATE",
    "protected": "PROTECTED",
    "sizeof": "SIZEOF",
    "static": "STATIC",
    "struct": "STRUCT",
    "template": "TEMPLATE",
    "this": "THIS",
    "throw": "THROW",
    "try": "TRY",
    "typedef": "TYPEDEF",
    "typename": "TYPENAME",
    "union": "UNION",
    "using": "USING",
    "virtual": "VIRTUAL",
    "bool": "BOOL",
    "char": "CHAR",
    "int": "INT",
    "long": "LONG",
    "double": "DOUBLE",
    "float": "FLOAT",
    "short": "SHORT",
    "void": "VOID",
    "__declspec": "IGNORE",
    "volatile": "IGNORE",
    "typeid": "IGNORE",
    "mutable": "IGNORE",
    "explicit": "IGNORE",
    "friends": "IGNORE",
    "register": "IGNORE",
    "unsigned": "IGNORE",
    "signed": "IGNORE",
    "__based": "IGNORE",
    "__cdecl": "IGNORE",
    "__except": "IGNORE",
    "__finally": "IGNORE",
    "__inline": "IGNORE",
    "__attribute": "IGNORE",
    "__attribute__": "IGNORE",
    "_based": "IGNORE",
    "__stdcall": "IGNORE",
    "__try": "IGNORE",
    "dllexport": "IGNORE",
    "final": "IGNORE",
    "override": "IGNORE",
    "noexcept": "IGNORE",
}


def t_IGNORE(t):
    r"__attribute\(.*\)|__section\(.*\)"
    return t


def t_LINEFEED(t):
    r"[\n]+"
    t.lexer.lineno += t.value.count("\n")
    return t


def t_SPACE(t):
    r"[ \t]+"
    return t


t_PREPROCESSORNEXT = r"\\"

t_NUMBER = r"[0-9][0-9XxA-Fa-fL]*"

t_SHARPSHARP = r"\#\#"

t_SHARP = r"\#"

# String literal


def t_STRING(t):
    r'"([^\\]|(\\.)|(\\\n))*?"'
    t.lexer.lineno += t.value.count("\n")
    return t


# Character constant 'c' or L'c'
t_CHARACTER = r"(L)?\'([^\\\n]|(\\.))*?\'"

# Comment (C-Style)


def t_COMMENT(t):
    r"/\*(.|\n)*?\*/"
    t.lexer.lineno += t.value.count("\n")
    if Search(r"/\*\*\s", t.value):
        t.additional = "DOXYGEN_JAVADOC"
    elif Search(r"/\*\!\s", t.value):
        t.additional = "DOXYGEN_QT"
    return t


# Comment (C++-Style)


def t_CPPCOMMENT(t):
    r"//.*"
    if Search(r"^///\b", t.value):
        t.additional = "DOXYGEN_CPP"
    if Search(r"^///<", t.value):
        t.additional = "DOXYGEN_POST"

    return t


def t_error(t):
    console.Out.Verbose(f"Illegal character '{t.value[0]}'", t.lexer.lineno)
    t.lexer.skip(1)


class CppLexerNavigator:
    """
    Main class for Cpp Lexer
    """

    def __init__(self, filename, data=None):
        self.filename = filename
        self.tokenlist = []
        self.indexstack = []
        self.tokenindex = -1
        self.matchingPair = {}
        self.reverseMatchingPair = {}
        self.ifdefstack = []
        import nsiqcppstyle_lexer

        lexer = nsiqcppstyle_lexer.lex()
        self.data = data
        if data is None:
            encoding = self.DetectEncoding(file_path=filename)
            with open(filename, "r", encoding=encoding) as f:
                try:
                    self.data = f.read()
                except UnicodeDecodeError as ex:
                    console.Out.Ci("[ERROR] UnicodeDecodeError in CppLexerNavigator: " + str(ex))
                    console.Out.Ci(
                        f"[ERROR] Exception occurred reading file '{filename}', convert from UTF16LE to UTF8",
                    )
                    raise
        self.lines = self.data.splitlines()
        lexer.input(self.data)
        index = 0
        while True:
            tok = lexer.token()
            if not tok:
                break
            tok.column = self._GetColumn(tok)
            tok.index = index
            tok.inactive = False
            index += 1
            self.tokenlist.append(tok)
            tok.line = self.lines[tok.lineno - 1]
            tok.filename = self.filename
            tok.pp = None
        #                self.ProcessIfdef(tok)
        self.PushTokenIndex()
        while True:
            t = self.GetNextToken()
            if t is None:
                break
            t.inactive = self.ProcessIfdef(t)
        self.PopTokenIndex()

    @property
    def tokenlistsize(self):
        return len(self.tokenlist)

    def ProcessIfdef(self, token):
        if token.type == "PREPROCESSOR":
            if Match(r"^#\s*if(n)?def$", token.value):
                self.ifdefstack.append(True)
            elif Match(r"^#\s*if$", token.value):
                nextToken = self.PeekNextTokenSkipWhiteSpaceAndComment()
                if nextToken is not None and nextToken.value == "0":
                    self.ifdefstack.append(False)
                else:
                    self.ifdefstack.append(True)
            elif Match(r"^#\s*endif$", token.value) and len(self.ifdefstack) != 0:
                self.ifdefstack.pop()
        return any(not ifdef for ifdef in self.ifdefstack)

    def Backup(self):
        """
        Back up the current context in lexer to be restored later
        """
        return (self.tokenindex, self.indexstack[:])

    def Restore(self, data):
        """
        Restore the lexer context.
        tuple using tokenindex and indexstack should be passed
        """
        self.tokenindex = data[0]
        self.indexstack = data[1]

    def Reset(self):
        """
        Reset Lexer
        """
        self.tokenindex = -1
        self.indexstack = []

    def GetCurTokenLine(self):
        """
        Get Current Token, if No current token, return None
        """
        curToken = self.GetCurToken()
        if curToken is not None:
            return self.lines[curToken.lineno - 1]
        return None

    def _MoveToToken(self, token):
        self.tokenindex = token.index

    def _GetColumn(self, token):
        """
        Get given token column
        """
        last_cr = self.data.rfind("\n", 0, token.lexpos)
        if last_cr < 0:
            last_cr = -1
        column = token.lexpos - last_cr
        if column == 0:
            return 1
        return column

    def GetCurToken(self):
        """
        Get Current Token
        """
        return self.tokenlist[self.tokenindex]

    def PushTokenIndex(self):
        """
        Push Current Token Index into stack to keep current token.
        """
        self.indexstack.append(self.tokenindex)

    def PopTokenIndex(self):
        """
        Pop token index stack to roll back to previously pushed token
        """
        self.tokenindex = self.indexstack.pop()

    def GetNextTokenSkipWhiteSpace(self):
        """
        Get Next Token skip the white space.
        """
        return self.GetNextToken(True)

    def PeekNextToken(self):
        self.PushTokenIndex()
        token = self._GetNextToken()
        self.PopTokenIndex()
        return token

    def PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess(self, offset=1):
        """
        Get Next Token skip whitespace, comment and preprocess.
        This method doesn't change the current lex position.
        """
        self.PushTokenIndex()
        token = None
        for _x in range(offset):  # @UnusedVariable
            token = self.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
        self.PopTokenIndex()
        return token

    def PeekNextTokenSkipWhiteSpaceAndComment(self):
        """
        Get Next Token skip whitespace and comment.
        This method doesn't change the current lex position.
        """
        self.PushTokenIndex()
        token = self.GetNextTokenSkipWhiteSpaceAndComment()
        self.PopTokenIndex()
        return token

    def PeekPrevToken(self):
        self.PushTokenIndex()
        token = self._GetPrevToken()
        self.PopTokenIndex()
        return token

    def PeekPrevTokenSkipWhiteSpaceAndCommentAndPreprocess(self, offset=1):
        """
        Get Previous Token skip whitespace and comment.
        This method doesn't change the current lex position.
        """
        self.PushTokenIndex()
        token = None
        for _x in range(offset):  # @UnusedVariable
            token = self.GetPrevTokenSkipWhiteSpaceAndCommentAndPreprocess()
        self.PopTokenIndex()
        return token

    def PeekPrevTokenSkipWhiteSpaceAndComment(self):
        """
        Get Previous Token skip whitespace and comment.
        This method doesn't change the current lex position.
        """
        self.PushTokenIndex()
        token = self.GetPrevTokenSkipWhiteSpaceAndComment()
        self.PopTokenIndex()
        return token

    def GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess(self):
        """
        Get Next Token skip whitespace, comment, preprocess
        This method changes the current lex position.
        """

        return self.GetNextToken(True, True, True)

    def GetNextTokenSkipWhiteSpaceAndComment(self):
        """
        Get Next Token skip whitespace and comment.
        This method changes the current lex position.
        """

        return self.GetNextToken(True, True)

    def GetPrevTokenSkipWhiteSpaceAndCommentAndPreprocess(self):
        """
        Get Previous Token skip whitespace, comment, process.
        This method changes the current lex position.
        """
        return self.GetPrevToken(True, True, True)

    def GetPrevTokenSkipWhiteSpaceAndComment(self):
        """
        Get Previous Token skip whitespace and comment.
        This method changes the current lex position.
        """
        return self.GetPrevToken(True, True)

    def GetNextToken(self, skipWhiteSpace=False, skipComment=False, skipDirective=False, skipMatchingBraces=False):
        """
        Get Next Token with various option
        - skipWhiteSpace - skip white space
        - skipComment - skip comment
        - skipDirective - skip preprocessor line
        - skipMatchingBraces - skip all { [ ( and matching pair
        """
        context = self._SkipContext(skipWhiteSpace, skipComment)
        while True:
            token = self._GetNextToken()
            if token is None:
                return token
            if token.inactive is True:
                continue
            if skipMatchingBraces and token.type in ["LPAREN", "LBRACE", "LBRACKET"]:
                self.GetNextMatchingToken()
                continue
            if skipDirective and token.pp is True:
                continue
            if token.type not in context:
                if token is not None:
                    token.column = self._GetColumn(token)
                return token

    def GetNextMatchingGT(self, keepCur=False):
        if keepCur:
            self.PushTokenIndex()
        gtStack = []
        if self.GetCurToken().type != "LT":
            msg = "Matching next GT token should be examined when cur token is <"
            raise RuntimeError(msg)
        gtStack.append(self.GetCurToken())
        t = self._GetNextMatchingGTToken(gtStack)
        if keepCur:
            self.PopTokenIndex()
        return t

    def _GetNextMatchingGTToken(self, tokenStack):
        while True:
            nextToken = self._GetNextToken()
            if nextToken is None:
                return None
            if nextToken.type in ["LT"]:
                tokenStack.append(nextToken)

            elif nextToken.type in ["GT"]:
                tokenStack.pop()
                if len(tokenStack) == 0:
                    return nextToken
            elif nextToken.type in ["RSHIFT"]:
                tokenStack.pop()
                if len(tokenStack) == 0:
                    return nextToken
                tokenStack.pop()
                if len(tokenStack) == 0:
                    return nextToken

    def GetNextMatchingToken(self, keepCur=False):
        """
        Get matching token
        """
        if keepCur:
            self.PushTokenIndex()
        tokenStack = []
        if self.GetCurToken().type not in ["LPAREN", "LBRACE", "LBRACKET"]:
            msg = "Matching token should be examined when cur token is { [ ("
            raise RuntimeError(msg)
        tokenStack.append(self.GetCurToken())
        t = self._GetNextMatchingToken(tokenStack)
        if keepCur:
            self.PopTokenIndex()
        return t

    def _GetNextMatchingToken(self, tokenStack):
        searchToken = tokenStack[-1]
        matchingToken = self.matchingPair.get(searchToken, None)
        lastPopedToken = None
        if matchingToken is not None:
            self._MoveToToken(matchingToken)
            return matchingToken
        while True:
            nextToken = self._GetNextToken()
            if nextToken is None:
                if lastPopedToken in self.reverseMatchingPair:
                    return None
                self.matchingPair[searchToken] = lastPopedToken
                self.reverseMatchingPair[lastPopedToken] = searchToken
                return lastPopedToken
            if nextToken.type in ["LPAREN", "LBRACE", "LBRACKET"]:
                tokenStack.append(nextToken)
                # print "Push", nextToken

            if nextToken.type in ["RPAREN", "RBRACE", "RBRACKET"]:
                prevTokenPair = tokenStack[-1]
                if prevTokenPair is not None:
                    if prevTokenPair.type[1:] == nextToken.type[1:]:
                        tokenStack.pop()
                        lastPopedToken = nextToken
                        if len(tokenStack) == 0:
                            if nextToken in self.reverseMatchingPair:
                                return None
                            self.matchingPair[searchToken] = nextToken
                            self.reverseMatchingPair[nextToken] = searchToken
                            return nextToken
                    else:
                        return None
                else:
                    return None

    def GetPrevTokenSkipWhiteSpace(self):
        return self.GetPrevToken(True)

    #    def GetPrevTokenSkipWhiteSpaceAndComment(self):
    #        return self.GetPrevToken(True, True)

    def GetPrevToken(self, skipWhiteSpace=False, skipComment=False, skipDirective=False, skipMatchingBraces=False):
        context = self._SkipContext(skipWhiteSpace, skipComment)
        while True:
            token = self._GetPrevToken()
            if token is None:
                return token
            if token.inactive:
                continue
            if skipMatchingBraces and token.type in ["RPAREN", "RBRACE", "RBRACKET"]:
                self.GetPrevMatchingToken()

                continue
            if skipDirective:
                line = self.GetCurTokenLine()
                if Search(r"^\s*#", line):
                    continue
            if token.type not in context:
                return token

    def GetPrevMatchingLT(self, keepCur=False):
        if keepCur:
            self.PushTokenIndex()
        gtStack = []
        if self.GetCurToken().type not in ["GT", "RSHIFT"]:
            msg = "Matching previous LT token should be examined when cur token is > or >>"
            raise RuntimeError(msg)
        # If >> token is found, append it twice
        if self.GetCurToken().type == "RSHIFT":
            gtStack.append(self.GetCurToken())
        gtStack.append(self.GetCurToken())
        t = self._GetPrevMatchingLTToken(gtStack)
        if keepCur:
            self.PopTokenIndex()
        return t

    def _GetPrevMatchingLTToken(self, tokenStack):
        while True:
            prevToken = self._GetPrevToken()
            if prevToken is None:
                return None
            if prevToken.type in ["GT"]:
                tokenStack.append(prevToken)
            elif prevToken.type in ["RSHIFT"]:
                tokenStack.append(prevToken)
                tokenStack.append(prevToken)
            elif prevToken.type in ["LT"]:
                tokenStack.pop()
                if len(tokenStack) == 0:
                    return prevToken

    def GetPrevMatchingToken(self, keepCur=False):
        if keepCur:
            self.PushTokenIndex()
        tokenStack = []
        if self.GetCurToken().type not in ["RPAREN", "RBRACE", "RBRACKET"]:
            msg = "Matching token should be examined when cur token is } ) ]"
            raise RuntimeError(msg)
        tokenStack.append(self.GetCurToken())

        t = self._GetPrevMatchingToken(tokenStack)
        if keepCur:
            self.PopTokenIndex()
        return t

    def _GetPrevMatchingToken(self, tokenStack):
        searchToken = tokenStack[-1]
        matchingToken = self.reverseMatchingPair.get(searchToken, None)
        if matchingToken is not None:
            self._MoveToToken(matchingToken)
            return matchingToken
        while True:
            prevToken = self._GetPrevToken()
            if prevToken is None:
                return None
            if prevToken.type in ["RPAREN", "RBRACE", "RBRACKET"]:
                tokenStack.append(prevToken)
                # print "Push", nextToken

            elif prevToken.type in ["LPAREN", "LBRACE", "LBRACKET"]:
                prevTokenPair = tokenStack[-1]
                if prevTokenPair is not None:
                    if prevTokenPair.type[1:] == prevToken.type[1:]:
                        tokenStack.pop()
                        # print "Pop", nextToken
                        # print tokenStack
                        if len(tokenStack) == 0:
                            self.reverseMatchingPair[searchToken] = prevToken
                            self.matchingPair[prevToken] = searchToken
                            return prevToken
                    else:
                        return None
                else:
                    return None

    def _SkipContext(self, skipWhiteSpace=False, skipComment=False):
        context = []
        if skipWhiteSpace:
            context.append("SPACE")
            context.append("LINEFEED")
        if skipComment:
            context.append("COMMENT")
            context.append("CPPCOMMENT")
        return context

    def _GetNextToken(self):
        if self.tokenindex < self.tokenlistsize - 1:
            self.tokenindex = self.tokenindex + 1
            return self.tokenlist[self.tokenindex]
        return None

    def _GetPrevToken(self):
        if self.tokenindex >= 0:
            self.tokenindex = self.tokenindex - 1
            if self.tokenindex == -1:
                return None
            return self.tokenlist[self.tokenindex]
        return None

    def GetPrevTokenInType(self, type, keepCur=True, skipPreprocess=True):
        if keepCur:
            self.PushTokenIndex()
        token = None
        while True:
            token = self.GetPrevToken()
            if token is None:
                break
            if token.type == type:
                if skipPreprocess and token.pp:
                    continue
                break
        if keepCur:
            self.PopTokenIndex()
        return token

    def GetPrevTokenInTypeList(self, typelist, keepCur=True, skipPreprocess=True):
        if keepCur:
            self.PushTokenIndex()
        token = None
        while True:
            token = self.GetPrevToken(False, False, skipPreprocess, False)
            if token is None:
                break
            if token.type in typelist:
                if skipPreprocess and token.pp:
                    continue
                break
        if keepCur:
            self.PopTokenIndex()
        return token

    def MoveToNextToken(self):
        if self.tokenindex < self.tokenlistsize - 1:
            self.tokenindex = self.tokenindex + 1

    def MoveToPrevToken(self):
        if self.tokenindex > 0:
            self.tokenindex = self.tokenindex - 1

    def GetNextTokenInType(self, type, keepCur=False, skipPreprocess=True):
        if keepCur:
            self.PushTokenIndex()
        token = None
        while True:
            token = self.GetNextToken()
            if token is None:
                break
            if token.type == type:
                if skipPreprocess and token.pp:
                    continue
                break
        if keepCur:
            self.PopTokenIndex()
        return token

    def GetNextTokenInTypeList(self, typelist, keepCur=False, skipPreprocess=True):
        if keepCur:
            self.PushTokenIndex()
        token = None
        while True:
            token = self.GetNextToken()
            if token is None:
                break
            if token.type in typelist:
                if skipPreprocess and token.pp:
                    continue
                break
        if keepCur:
            self.PopTokenIndex()
        return token

    def HasBody(self):
        if self.GetCurToken() is None:
            return False
        token_id2 = self.GetNextTokenInType("LBRACE", True)
        token_id3 = self.GetNextTokenInType("SEMI", True)

        if token_id3 is None and token_id2 is not None:
            return True
        return bool(token_id2 is not None and token_id2.lexpos < token_id3.lexpos)

    def DetectEncoding(self, file_path):
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            if result['encoding'] is not None and result['confidence'] > 0.9:
                return result['encoding']
            else:
                return "utf-8"


class Context:
    def __init__(self, type, name, sig=False, starttoken=None, endtoken=None):
        self.type = type
        self.name = name
        self.sig = sig
        self.startToken = starttoken
        self.endToken = endtoken
        self.additional = ""

    def __str__(self):
        return ", ".join([self.type, "'" + self.name + "'", str(self.startToken), str(self.endToken)])

    def IsContextStart(self, token):
        return token == self.startToken

    def IsContextEnd(self, token):
        return token == self.endToken

    def InScope(self, token):
        return bool(token.lexpos >= self.startToken.lexpos and token.lexpos <= self.endToken.lexpos)


class ContextStack:
    def __init__(self):
        self.contextstack = []

    def Push(self, context):
        self.contextstack.append(context)

    def Pop(self):
        if self.Size() == 0:
            return None
        return self.contextstack.pop()

    def Peek(self):
        if self.Size() == 0:
            return None
        return self.contextstack[-1]

    def SigPeek(self):
        i = len(self.contextstack)
        while True:
            if i == 0:
                break
            i -= 1
            if self.contextstack[i].sig:
                return self.contextstack[i]
        return None

    def Size(self):
        return len(self.contextstack)

    def IsEmpty(self):
        return len(self.contextstack) == 0

    def ContainsIn(self, type):
        i = len(self.contextstack)
        while True:
            if i == 0:
                break
            i -= 1
            if self.contextstack[i].type == type:
                return True
        return False

    def __str__(self):
        a = ""
        for eachContext in self.contextstack:
            a += eachContext.__str__() + " >> "
        return a

    def Copy(self):
        contextStack = ContextStack()
        contextStack.contextstack = self.contextstack[:]
        return contextStack


class _ContextStackStack:
    def __init__(self):
        self.contextstackstack = []

    def Push(self, contextstack):
        self.contextstackstack.append(contextstack)

    def Pop(self):
        if len(self.contextstackstack) == 0:
            return None
        return self.contextstackstack.pop()

    def Peek(self):
        if len(self.contextstackstack) == 0:
            return None
        return self.contextstackstack[-1]


############################################################################
# Parser and Rule Runner Invocator
############################################################################
# AddLineRule(lineRule)


def ProcessFile(ruleManager, file, data=None):
    #    print file
    try:
        lexer = CppLexerNavigator(file, data)
    except UnicodeDecodeError:
        # If an exception was thrown (i.e., UnicodeDecodeError), it was
        # caught, process, logged to stdout, and the exception was raised
        # again.  At this point in the code, there is nothing else to do
        # other than skip the processing of the file, which is why we
        # just return.
        return
    ConstructContextInfo(lexer)
    # Run Rules
    lexer.Reset()
    RunRules(ruleManager, lexer)


def ConstructContextInfo(lexer):
    #    classstate = None
    #    depth = 0
    contextStack = ContextStack()
    contextStackStack = _ContextStackStack()
    contextStackStack.Push(contextStack)
    contextPrediction = None
    ppScope = False
    prevLine = 0
    templateContext = None
    nsiqcppstyle_state._nsiqcppstyle_state.ResetRuleSuppression()
    comment = lexer.GetNextTokenInTypeList(("COMMENT", "CPPCOMMENT"), True)
    if comment is not None:
        for e in FindAll(r"--\s*(RULE\w*)", comment.value):
            nsiqcppstyle_state._nsiqcppstyle_state.SuppressRule(e)
    t = None
    # Construct Context
    while True:
        try:
            t = lexer.GetNextTokenSkipWhiteSpaceAndComment()
            if t is None:
                break
            t.contextStack = None
            t.context = None

            if t.type == "PREPROCESSOR":
                t.pp = True
                ppScope = True
            elif ppScope is True:
                if prevLine == t.lineno - 1:
                    prevToken = lexer.PeekPrevTokenSkipWhiteSpaceAndComment()
                    if prevToken is not None:
                        ppScope = prevToken.type == "PREPROCESSORNEXT"
                    t.pp = ppScope
                elif prevLine == t.lineno:
                    t.pp = True
                else:
                    ppScope = False

            if templateContext is not None and not templateContext.InScope(t):
                templateContext = None

            if t.type in ["LBRACE", "LPAREN", "LBRACKET"]:
                if contextPrediction is not None and contextPrediction.IsContextStart(t):
                    contextStack = contextStack.Copy()
                    contextStack.Push(contextPrediction)
                    contextStackStack.Push(contextStack)
                    contextPrediction = None
                else:
                    mt = lexer.GetNextMatchingToken(True)
                    if mt is not None:
                        contextStack = contextStack.Copy()
                        contextStack.Push(Context(t.type[1:] + "BLOCK", "", False, t.lexpos, mt.lexpos))
                        contextStackStack.Push(contextStack)

            #       print depth, "Push", contextStack
            elif t.type in ["RBRACE", "RPAREN", "RBRACKET"]:
                contextStackStack.Pop()
                contextStack = contextStackStack.Peek()
                # print depth, "Pop ", contextStack
            # Type Prediction
            elif t.type == "TEMPLATE":
                lexer.PushTokenIndex()
                t2 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()

                if t2 is not None and t2.type == "LT":
                    t3 = lexer.GetNextMatchingGT()
                    templateContext = Context("TEMPLATE", "", False, t2, t3)

                lexer.PopTokenIndex()
            elif (
                t.pp is not True
                and templateContext is None
                and t.type in ["CLASS", "STRUCT", "ENUM", "UNION", "NAMESPACE"]
                and contextPrediction is None
            ):
                prevToken = lexer.PeekPrevTokenSkipWhiteSpaceAndCommentAndPreprocess()
                hasBody = lexer.HasBody()
                fullName = ""
                curContext = contextStack.Peek()
                if (
                    (prevToken is None or prevToken.value != "<")
                    and (curContext is None or curContext.type != "PARENBLOCK")
                    and hasBody
                ):
                    lexer.PushTokenIndex()
                    # find start and end brace block
                    contextStart = lexer.GetNextTokenInType("LBRACE")
                    contextEnd = lexer.GetNextMatchingToken(contextStart)
                    lexer.PopTokenIndex()
                    lexer.PushTokenIndex()

                    if contextEnd is not None:
                        while True:
                            token = lexer.GetNextTokenInType("ID")
                            nextIDtoken = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
                            if token is None or token.lexpos > contextStart.lexpos:
                                break
                            if nextIDtoken.type == "ID":
                                continue
                            nextToken = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
                            if token is not None and nextToken is not None and nextToken.type == "DOUBLECOLON":
                                fullName += token.value + "::"
                                continue
                            fullName += token.value
                            break
                        contextPrediction = Context(t.type + "_BLOCK", fullName, True, contextStart, contextEnd)
                    lexer.PopTokenIndex()
                t.type = "TYPE"
                t.fullName = fullName
                t.context = contextPrediction
                t.decl = not hasBody
            #   RunTypeRule(lexer, fullName, not hasBody, contextStack, contextPrediction)

            # Function Prediction
            elif t.pp is not True and t.type in ("ID", "OPERATOR") and contextPrediction is None:
                operator_name = None
                curNotSigContext = contextStack.Peek()
                if curNotSigContext is not None and curNotSigContext.sig is False:
                    continue
                t2 = None
                t4 = None
                if t.type == "ID":
                    t2 = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
                    t4 = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess(2)
                else:
                    t2 = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
                    operator_name = deepcopy(t2)
                    if t2.type == "LPAREN":
                        operator_name.value = "()"  # call operator
                        operator_name.type = "PARENS"  # call operator
                        t2 = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess(3)
                        t4 = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess(4)
                    else:
                        t2 = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess(2)
                        t4 = lexer.PeekNextTokenSkipWhiteSpaceAndCommentAndPreprocess(3)

                t3 = lexer.PeekPrevTokenSkipWhiteSpaceAndCommentAndPreprocess()
                curContext = contextStack.SigPeek()

                if (
                    (t3 is None or t3.type != "NEW")
                    and t2 is not None
                    and t2.type == "LPAREN"
                    and t4.type != "STRING"
                    and (curContext is None or curContext.type in ["CLASS_BLOCK", "STRUCT_BLOCK", "NAMESPACE_BLOCK"])
                ):
                    # Check The ID after the next RPAREN
                    # if there is ID, None, or LBRACKET it's not a function.
                    # in case HELLO() HELLO2(), or FOO (BAR*)[]
                    lexer.PushTokenIndex()
                    lexer._MoveToToken(t2)
                    lexer.GetNextMatchingToken()
                    t5 = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
                    if t5 is None or t5.type in ["ID", "LBRACKET"]:
                        lexer.PopTokenIndex()
                        continue
                    lexer.PopTokenIndex()
                    ##############################

                    lexer.PushTokenIndex()
                    contextPrediction = None
                    fullName = t.value
                    lexer.PushTokenIndex()
                    if t.type == "OPERATOR":
                        fullName = fullName + operator_name.value
                        t.value = t.value + operator_name.value
                        while True:
                            prevName = lexer.GetPrevTokenSkipWhiteSpaceAndCommentAndPreprocess()
                            if prevName is not None:
                                if prevName.type == "DOUBLECOLON":
                                    value_to_prepend = lexer.GetPrevTokenSkipWhiteSpaceAndCommentAndPreprocess().value
                                    fullName = f"{value_to_prepend}::{fullName}"
                                else:
                                    break
                            else:
                                break
                    else:
                        while True:
                            prevName = lexer.GetPrevTokenSkipWhiteSpaceAndCommentAndPreprocess()
                            if prevName is not None:
                                if prevName.type == "NOT":
                                    fullName = "~" + fullName
                                elif prevName.type == "DOUBLECOLON":
                                    value_to_prepend = lexer.GetPrevTokenSkipWhiteSpaceAndCommentAndPreprocess().value
                                    fullName = f"{value_to_prepend}::{fullName}"
                                else:
                                    break
                            else:
                                break
                    lexer.PopTokenIndex()
                    # if Match(r"^[A-Z_][A-Z_0-9][A-Z_0-9]+$", fullName):
                    #     continue
                    impl = lexer.HasBody()
                    if impl:
                        while True:
                            # handle ctor list initializers
                            contextStart = lexer.GetNextTokenInType("LBRACE")
                            if t.type != "ID" or prevName is None:
                                break
                            if curContext is not None and curContext.type in ["CLASS_BLOCK", "STRUCT_BLOCK"]:
                                # we are in a class
                                if t.value != curContext.name or fullName[0] == "~":
                                    break  # not a ctor
                            elif "::" in fullName:
                                # checking for a ctor outside a class
                                names = fullName.split("::")
                                if len(names) == 1 or names[-1] != names[0]:
                                    break
                            else:
                                # just a normal scope, no need to iterate
                                break
                            bracePrevToken = lexer.PeekPrevTokenSkipWhiteSpaceAndComment()
                            if bracePrevToken.type in ["RPAREN", "RBRACE", "COMMA"]:
                                # we reached the end of initializer list
                                break
                        contextEnd = lexer.GetNextMatchingToken(contextStart)
                        if contextEnd is not None:
                            contextPrediction = Context("FUNCTION_BLOCK", fullName, True, contextStart, contextEnd)

                    # RunFunctionRule(lexer, functionName, decl, contextStack, contextPrediction)
                    t.type = "FUNCTION"
                    t.fullName = fullName
                    t.context = contextPrediction
                    t.decl = not impl
                    lexer.PopTokenIndex()
                    if operator_name is not None:
                        operator_name = None
                    # print "TT", lexer.GetCurTokenLine(), impl,
                    # contextPrediction
            t.contextStack = contextStack
            prevLine = t.lineno
        except Exception as e:
            console.Err.Verbose("Context Construction Error : ", t, t.contextStack, e)
            console.Err.Verbose(traceback.format_exc())


def RunRules(ruleManager, lexer):
    try:
        ruleManager.RunFileStartRule(lexer, os.path.basename(lexer.filename), os.path.dirname(lexer.filename))
    except Exception as e:
        console.Err.Verbose("Rule Error : ", e)
        console.Err.Verbose(traceback.format_exc())
    currentLine = 0
    t = None
    while True:
        try:
            t = lexer.GetNextTokenSkipWhiteSpace()
            if t is None:
                break
            if currentLine != t.lineno:
                currentLine = t.lineno
                ruleManager.RunLineRule(lexer, lexer.GetCurTokenLine(), currentLine)

            if t.pp is True:
                ruleManager.RunPreprocessRule(lexer, t.contextStack)
            else:
                if t.type == "TYPE":
                    ruleManager.RunTypeNameRule(lexer, t.value.upper(), t.fullName, t.decl, t.contextStack, t.context)
                elif t.type == "FUNCTION":
                    ruleManager.RunFunctionNameRule(lexer, t.fullName, t.decl, t.contextStack, t.context)
                elif t.type in ("COMMENT", "CPPCOMMENT"):
                    ruleManager.RunCommentRule(lexer, t)
                    continue
                elif t.contextStack is not None and t.contextStack.SigPeek() is not None:
                    sigContext = t.contextStack.SigPeek()
                    if sigContext.type == "FUNCTION_BLOCK":
                        ruleManager.RunFunctionScopeRule(lexer, t.contextStack)
                    elif sigContext.type in [
                        "CLASS_BLOCK",
                        "STRUCT_BLOCK",
                        "ENUM_BLOCK",
                        "NAMESPACE_BLOCK",
                        "UNION_BLOCK",
                    ]:
                        ruleManager.RunTypeScopeRule(lexer, t.contextStack)

                ruleManager.RunRule(lexer, t.contextStack)
        except Exception as e:
            console.Err.Verbose("Rule Error : ", t, t.contextStack, e)
            console.Err.Verbose(traceback.format_exc())
    try:
        ruleManager.RunFileEndRule(lexer, os.path.basename(lexer.filename), os.path.dirname(lexer.filename))
    except Exception as e:
        console.Err.Verbose("Rule Error : ", e)
        console.Err.Verbose(traceback.format_exc())