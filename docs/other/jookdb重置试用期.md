将下面的内容保存在 jookdb重置试用期.bat 文件中,把bat文件放到与jookdb.exe同级目录下
```
@echo off
:: 请求管理员权限（如果需要）
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 当前未以管理员权限运行，正在请求管理员权限...
    PowerShell Start-Process "%~f0" -Verb RunAs
    exit /b
)

:: 获取当前批处理文件所在的目录
set current_dir=%~dp0

:: 判断当前目录下是否存在 jookdb.exe
if exist "%current_dir%jookdb.exe" (
    echo 文件 jookdb.exe 存在于当前目录。%current_dir%jookdb.exe

    :: 删除注册表项 HKEY_CURRENT_USER\SOFTWARE\jookdb
    echo 正在删除注册表项 HKEY_CURRENT_USER\SOFTWARE\jookdb...
    reg delete "HKEY_CURRENT_USER\SOFTWARE\jookdb" /f >nul 2>&1
    if %errorlevel% equ 0 (
        echo 注册表项删除成功。
    ) else (
        echo 注册表项删除失败，可能该注册表项不存在。
    )

    :: 构造完整的值名称（当前目录路径 + jookdb.exe）
    set value_name=%current_dir%jookdb.exe

    :: 删除注册表中的指定值
    echo 正在删除注册表中的值: %current_dir%jookdb.exe
    reg delete "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store" /v "%current_dir%jookdb.exe" /f >nul 2>&1
    if %errorlevel% equ 0 (
        echo 注册表值删除成功。
    ) else (
        echo 注册表值删除失败，可能该值不存在。
    )
    reg delete "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FeatureUsage\AppSwitched" /v "%current_dir%jookdb.exe" /f >nul 2>&1
    if %errorlevel% equ 0 (
        echo 注册表值删除成功。
    ) else (
        echo 注册表值删除失败，可能该值不存在。
    )
    reg delete "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FeatureUsage\ShowJumpView" /v "%current_dir%jookdb.exe" /f >nul 2>&1
    if %errorlevel% equ 0 (
        echo 注册表值删除成功。
    ) else (
        echo 注册表值删除失败，可能该值不存在。
    )
) else (
    echo 文件 jookdb.exe 不存在于当前目录。
)

pause
exit
```

加入定时任务
```
schtasks /create /tn "重置jookdb试用期" /tr "jookdb重置试用期.bat路径" /sc weekly /d MON /st 12:00 /ru "SYSTEM"
```