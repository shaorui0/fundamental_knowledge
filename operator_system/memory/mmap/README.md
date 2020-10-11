记录：
- `simple_anonymous_set_zero.c`里，`mmap`功能类似`malloc(5 int)` + `mmset(0)`

运行过程中出现错误的地方：
- 如果`read_from_fd.c`里面`MAP_PRIVATE`改为`MAP_SHARED`将导致`Mapping Failed`，而`ipc*.c`则能正确运行，想清楚这个flag的意义。


