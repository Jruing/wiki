```
package pkg

import (
	"fmt"
	"log"
	"log/slog"
	"os"
	"time"
)

var controlLogger *slog.Logger
var fileLogger *slog.Logger

const (
	timeFormat = "2006-01-02"
)

func InitLog(filepath string) {
	options := slog.HandlerOptions{
		// 是否打印文件名称及行号
		AddSource: false,
		Level:     slog.LevelDebug,
		ReplaceAttr: func(groups []string, a slog.Attr) slog.Attr {
			if a.Key == slog.TimeKey {
				a.Value = slog.AnyValue(time.Now().Format("2006-01-02 15:04:05"))
			}
			return a
		},
	}
	// 打开文件
	file, err := os.OpenFile(filepath, os.O_WRONLY|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		fmt.Println(err)
	}
	// 文件写入
	fileLogger = slog.New(slog.NewJSONHandler(file, &options))
	// 控制台输出
	controlLogger = slog.New(slog.NewTextHandler(os.Stdout, &options))

	// 启动定时器，每天零点进行日志轮转
	startTimer(file, filepath)
}

// 计时器
func startTimer(fileObj *os.File, filepath string) {
	now := time.Now()
	//// 计算下一分钟的开始时间
	//next := now.Truncate(time.Minute).Add(time.Minute)
	// 计算下一个零点时间
	next := now.Add(time.Hour * 24)
	next = time.Date(next.Year(), next.Month(), next.Day(), 0, 0, 0, 0, next.Location())
	// 计算当前时间到下一个零点的时间间隔
	timer := time.NewTimer(next.Sub(now))
	// 每秒钟
	//timer := time.NewTicker(time.Second)

	go func() {
		<-timer.C
		rotateLogs(fileObj, filepath)
		startTimer(fileObj, filepath)
	}()
}

// 日志轮转函数
func rotateLogs(fileObj *os.File, filepath string) {
	// 关闭当前的日志文件
	fileObj.Close()

	// 生成新的日志文件名
	newPath := fmt.Sprintf("%s_%s", filepath, time.Now().Format(timeFormat))

	// 将当前日志文件重命名为新的文件名
	err := os.Rename(filepath, newPath)
	if err != nil {
		log.Fatal("无法重命名日志文件:", err)
	}

	// 创建一个新的日志文件
	writer, err := os.OpenFile(filepath, os.O_WRONLY|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		log.Fatal("无法打开日志文件:", err)
	}
	options := slog.HandlerOptions{
		// 是否打印文件名称及行号
		AddSource: false,
		Level:     slog.LevelDebug,
		ReplaceAttr: func(groups []string, a slog.Attr) slog.Attr {
			if a.Key == slog.TimeKey {
				a.Value = slog.AnyValue(time.Now().Format("2006-01-02 15:04:05"))
			}
			return a
		},
	}
	// 设置日志输出到新的日志文件
	fileLogger = slog.New(slog.NewJSONHandler(writer, &options))
	// 控制台输出
	controlLogger = slog.New(slog.NewTextHandler(os.Stdout, &options))
}

func Info(msg string, args ...any) {
	controlLogger.Info(msg, args...)
	fileLogger.Info(msg, args...)
}

func Error(msg string, args ...any) {
	controlLogger.Error(msg, args...)
	fileLogger.Error(msg, args...)
}

func Debug(msg string, args ...any) {
	controlLogger.Debug(msg, args...)
	fileLogger.Debug(msg, args...)
}

func Warn(msg string, args ...any) {
	controlLogger.Warn(msg, args...)
	fileLogger.Warn(msg, args...)
}

```
