# SQL Directory

1、请删除 出了用户表以外的所有  dept_belong_id字段
2、请按照以下表的功能，重新设计rbac.sql 数据库表结构，删除冗余字段和索引
3、请注意，仅修改rbac.sql文件，其他文件请勿修改

system_config  系统配置表
system_deptinfo,  部门信息表
system_menu,   菜单表(对应权限)
system_menumeta, 菜单表元数据
system_operationlog,  操作记录，记录所有业务操作
system_userinfo,  用户信息表
system_userinfo_roles, 角色表
system_userloginlog,  用户登录记录表，记录用户登录和退出信息
system_userrole,  用户和角色的关联表
system_userrole_menu 角色和菜单的关联表