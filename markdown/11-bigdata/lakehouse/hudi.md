# Apache Hudi

Hudi 是湖仓表格式，重点解决数据湖中的 upsert、增量消费、近实时入湖和小文件管理问题。

## 表类型

- Copy On Write：写入时生成新的列式文件，读性能好，写放大较高。
- Merge On Read：增量写入 log 文件，读时合并 base file 和 log，写入延迟低。

## 核心概念

- Record Key：记录唯一键。
- Precombine Field：同一 key 多条记录时选择最新记录。
- Partition Path：分区路径。
- Timeline：记录 commit、clean、compaction 等操作。
- Index：定位记录所在文件，支持 upsert。

## 写入模式

- Insert：只新增。
- Upsert：按主键更新或插入。
- Bulk Insert：大批量初始化导入。
- Delete：删除记录。

## 适合场景

- CDC 入湖。
- 需要增量查询的离线/准实时链路。
- 用户画像、订单状态、维表快照。
- 需要处理更新和删除的数据湖。

## Hudi 与 Iceberg

- Hudi 更强调 upsert、增量拉取和写入服务。
- Iceberg 更强调开放标准、多引擎兼容、快照和分区演进。
- 选型要看是否高频更新、是否需要增量消费、查询引擎生态和团队经验。

## 面试重点

Hudi 的核心不是“把文件放到 HDFS”，而是通过 Timeline、Index、Record Key 和表服务，让数据湖支持更新、增量和近实时消费。
