# TCP 状态机

```
client          server

                LISTEN
SYN_SEND
                SYN_RCVD
ESTABLISHED 
                ESTABLISHED 

FIN_WAIT_1
                CLOSE_WAIT
FIN_WAIT_2  
                LAST_ACK
TIME_WAIT( 2 MSL )
```

## Why TIME_WAIT state need to be 2MSL long?


挥手过程：

1. client -> server, FIN
2. server -> client, ACK
3. server -> client, FIN
4. client -> server, ACK

> After above 4 steps, client is TIME_WAIT, server is LAST_ACK

如果第四步丢了（client不知道自己的ACK丢了），则需要第三步重试。
这里的2 MSL就是给一次3过程，给一次4 redo 过程。
整体就是 client 等最后一个 ACK 发过去，如果失败，再等 server 发一个 FIN 过来。

[why-time-wait-state-need-to-be-2msl-long](https://stackoverflow.com/questions/25338862/why-time-wait-state-need-to-be-2msl-long)

### what if step 4 is lost again?

> Same as with any data segment. TCP will retry the send a certain number of times and then reset the connection.

重试一段时间后 reset 连接。

[how-if-the-last-ack-is-lost-in-tcp-termination](https://stackoverflow.com/questions/40417087/how-if-the-last-ack-is-lost-in-tcp-termination)