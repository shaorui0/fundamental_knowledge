# What is Protobuf?

NOTICE: the protobuf **is not for humans**, serialized data is compiled bytes and hard for the human reading. There are two ways to solve it: 

1. read strcture of proto by watching the .proto file, pay attention to keywords 'optional'(not in **pb3**).

2. MessageToJson

```py
from google.protobuf.json_format import MessageToJson
jsonObj = MessageToJson(pb)
```



# why protobuf?

Some scenarios require **schema** (Define once, use everywhere).
【速度】
- 编解码的方式和传统的二进制不太一样，
- 三个部分分别是长度、key_num、value（这样编解码起来快了很多），主要节省的地方就在key不用使用字符串，同时长度是固定的，直接读就行，而不需要通过解析，比如遇到括号或者逗号这样
- float在json中的编解码也慢（not designed for numbers）

【schema带来的】
- easier to bind to objects；json是典型的string。

【可读性】
- json更可读

【普适性】
pb基本使用量级是赶不上json的

https://www.bizety.com/2018/11/12/protocol-buffers-vs-json/#:~:text=Protobuf%20is%20easier%20to%20bind,is%20not%20designed%20for%20numbers.&text=The%20library%20implementation%20for%20Protobuf,be%20a%20faster%20format%20overall

### pros

think XML, but smaller, faster, and simpler(really?).

- Performance:
    - **easier to bind to objects** and faster.
    - As JSON is textual, its **integers** and **floats** can be slow to encode and decode.
- Smaller size(*why faster than Json?*):
    - Protobuf binary format Serialization
    - Benchmark see [faster than json - Benchmark](https://blog.usejournal.com/what-the-hell-is-protobuf-4aff084c5db4)）
- Others:
    - RPC support


### cons(JSON can solve it)

- JSON is widely accepted by almost all programming languages and highly popular.
- Non-human readability
- Data from the service is directly consumed by a web browser
- Your server side application is written in JavaScript
- You aren’t prepared to tie the data model to a schema
- You don’t have the bandwidth to add another tool to your arsenal
- The operational burden of running a different kind of network service is too great


### 优势 TODO

# protobuf有什么优势？

0. JSON没有紧凑的动作，单个pack数据量也比较大
1. PB编解码速度快，有schema，二进制过程进行了“紧凑”（典型就是
2. 向前兼容（旧代码也能读新数据），当然，这需要在修改schema定义的时候，有注意事项。比如数字不能瞎改、不能删除required等
    field_tag(replace key_content) + type + length + value_content
    这就意味着：
    - 可以更改key的名称（field_tag只记录了数字），那显然的，数字不能修改
    - 添加字段只能是可选的，或者具有默认值
    - repeated的设计思想在于“前后兼容性”
        - optional => repeated
        - 旧代码看新数据，只能看到最后一个元素
        - 新代码看旧数据，看到的是0/1个元素的list
3. 向后兼容（代码通常更新最快，数据可能也会跟着更新，但是会不会有旧数据过来？比如说上游，比如说协调还没有完全一致）

4. 支持的数据格式也比较多，JSON对数字（整数、浮点数）支持不好，编解码速度也会比较慢

https://www.bizety.com/2018/11/12/protocol-buffers-vs-json/#:~:text=Protobuf%20is%20easier%20to%20bind,is%20not%20designed%20for%20numbers.&text=The%20library%20implementation%20for%20Protobuf,be%20a%20faster%20format%20overall

https://vonng.gitbooks.io/ddia-cn/content/ch4.html
# how to use

```
ls *.proto | awk '{print "protoc -I=. --python_out=. ./"$0}' | sh
```

## proto message parse

### recursive resolution based on DESCRIPTOR.fields

```py
def dump_object(obj):
    for descriptor in obj.DESCRIPTOR.fields:
        value = getattr(obj, descriptor.name)
        if descriptor.type == descriptor.TYPE_MESSAGE:
            if descriptor.label == descriptor.LABEL_REPEATED:
                map(dump_object, value)
            else:
                dump_object(value)
        elif descriptor.type == descriptor.TYPE_ENUM:
            pass
        else:
            if descriptor.type == descriptor.TYPE_BYTES:
                # TODO 转码
                pass
            else:
                pass
```

### iterative resolution based on proto schema

```py

def parse_general_field(pb):
    if len(pb.general_ad_field.ad_packs) == 0:
        return []

    product_id = pb.product_id
    sub_app_id = pb.sub_app_id
    arr_material = []

    for ad_pack in pb.general_ad_field.ad_packs:
        user_id = str(get_user_id(ad_pack))
        for ad_elem in ad_pack.ad_elems_array:
            
            # 过滤非增量
            if ad_elem.element_result.audit_channel_type != ad_review_util_pb2.kAd_AutoIncreaseAudit:
               continue
            
            # 过滤非通过
            if ad_elem.element_result.review_result == ad_review_util_pb2.kAd_APPROVED:
               continue

            ad_id = get_ad_id(ad_elem)
            # 遍历不同类型的广告内容
            ad_content_fields = [
                "word_text_cont_array", "idea_text_cont_array",
            ]
            for ad_content_field in ad_content_fields:
                ad_contents = getattr(ad_elem, ad_content_field)
                # 遍历广告内容
                text_cont_list = []
                text_type = None
                for ad_content in ad_contents:
                    (ad_type, ad_cont) = get_ad_type_and_cont(ad_content, is_general=True)
                    if ad_type in ('word', 'idea'):
                        text_cont_list.append(ad_cont)
                        text_type = ad_type

                if len(text_cont_list) != 0:
                    arr_material.append((product_id, user_id, text_type, '  '.join(text_cont_list)))

    return arr_material
```

### run demo

```py
# -*- coding: utf-8 -*-
import sys

from proto_pb import ad_review_service_pb2
from proto_pb import ad_review_util_pb2
import hdfs_seq_file_reader


def do_item(key, value):
    """ do_item
        key: pipelet-point-seq, value:...
        return: pb
    """
    ads = ad_review_service_pb2.AdReviewService()
    ads.ParseFromString(value)

    print("{}".format(ads))
    return ads


if __name__ == '__main__':
    input_path = sys.argv[1]
    fin = hdfs_seq_file_reader.HdfsSeqfileReader(input_path)
    while (True):
        key, value = fin.get_next()
        if (key is None and value is None):
            break

        try:
            ret = do_item(key, value)

        except Exception as ex:
            print("key:{}, ex:{}".format(key, ex))

```


### parse HdfsSeqfile

```py
# -*- coding: utf-8 -*-

import sys
import struct

class HdfsSeqfileReader(object):
    """ HdfsSeqfileReader
    """
    def __init__(self, fpath):
        self.fn = fpath
        self.fin = open(self.fn)

    def get_next(self):
        """ get_next
            Return:
                (Key, Value)
        """
        key_len_byte = self.fin.read(4)
        if not key_len_byte:
            return (None, None)
        key_len = struct.unpack('<I', key_len_byte)[0]
        key_byte = self.fin.read(key_len)
        key_fm = '>%ds' % (key_len)
        key = struct.unpack(key_fm, key_byte)[0]
        val_len_byte = self.fin.read(4)
        val_len = struct.unpack('<I', val_len_byte)[0]
        val_byte = self.fin.read(val_len)
        val_fm = '>%ds' % (val_len)
        val = struct.unpack(val_fm, val_byte)[0]
        return (key, val)

```






# Ref

https://codeclimate.com/blog/choose-protocol-buffers/

