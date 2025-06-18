/*******************************************************************************
 *  Copyright (C) 2014-2023 Revopoint 3D Technologies Inc. All rights reserved. *
 *                                                                              *
 *  @file     CrashpadHelper.h                                                  *
 *  @brief    crashpad奔溃dump                                                  *
 *  Details.                                                                    *
 *                                                                              *
 *  @author   gcr                                                               *
 *  @version  1.0.0                                                             *
 *  @date     2025-02-12                                                        *
 *                                                                              *
 *------------------------------------------------------------------------------*
 *  Change History :                                                            *
 *  <Date>     | <Version> | <Author>       | <Description>                     *
 *------------------------------------------------------------------------------*
 *  2025-02-12 | 1.0.0     | gcr         | Create file                          *
 *------------------------------------------------------------------------------*
 *                                                                              *
 ********************************************************************************/
#include "CrashpadHelper.h"

#define NOMINMAX
#include <client/crash_report_database.h>
#include <client/crashpad_client.h>
#include <client/settings.h>

using namespace base;
using namespace crashpad;
using namespace std;

std::unique_ptr<crashpad::CrashReportDatabase> database;

bool CrashpadHelper::startCrashHandler(std::string const &url, StringType const &handler_path, StringType const &db_path)
{
    using namespace crashpad;

    std::map<std::string, std::string> annotations;
    std::vector<std::string> arguments;

    annotations["format"] = "minidump"; // 设置生成minidump
    arguments.push_back("--no-rate-limit"); // 禁用了崩溃速率限制

    base::FilePath db(db_path);
    base::FilePath handler(handler_path);

    database = crashpad::CrashReportDatabase::Initialize(db); // 打开一个崩溃报告数据库

    if (database == nullptr || database->GetSettings() == NULL) {
        return false;
    }
    database->GetSettings()->SetUploadsEnabled(true); // 启用自动上传。
    // 启动一个crash处理程序进程
    return CrashpadClient().StartHandler(handler, db, db, url, annotations, arguments, false, false, {});
}

#if defined(__APPLE__)
#include <mach-o/dyld.h>
#include <vector>

StringType CrashpadHelper::getExecutableDir()
{
    unsigned int bufferSize = 512;
    vector<char> buffer(bufferSize + 1);

    if (_NSGetExecutablePath(&buffer[0], &bufferSize)) {
        buffer.resize(bufferSize);
        _NSGetExecutablePath(&buffer[0], &bufferSize);
    }

    char *lastForwardSlash = strrchr(&buffer[0], '/');
    if (lastForwardSlash == NULL) return NULL;
    *lastForwardSlash = 0;

    return &buffer[0];
}
#elif defined(__linux__)
#include <stdio.h>
#include <unistd.h>
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

StringType CrashpadHelper::getExecutableDir()
{
    char pBuf[FILENAME_MAX];
    int len = sizeof(pBuf);
    int bytes = MIN(readlink("/proc/self/exe", pBuf, len), len - 1);
    if (bytes >= 0) {
        pBuf[bytes] = '\0';
    }

    char *lastForwardSlash = strrchr(&pBuf[0], '/');
    if (lastForwardSlash == NULL) return NULL;
    *lastForwardSlash = '\0';

    return pBuf;
}
#elif defined(_MSC_VER)
StringType CrashpadHelper::getExecutableDir()
{
    HMODULE hModule = GetModuleHandleW(NULL);
    WCHAR path[MAX_PATH];
    DWORD retVal = GetModuleFileNameW(hModule, path, MAX_PATH);
    if (retVal == 0) return NULL;

    wchar_t *lastBackslash = wcsrchr(path, '\\');
    if (lastBackslash == NULL) return NULL;
    *lastBackslash = 0;

    return path;
}
#endif