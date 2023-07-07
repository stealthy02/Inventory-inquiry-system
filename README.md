# Inventory-inquiry-system
这是一个简单查阅库存的系统,通过输入采购订单信息和销售订单信息确定库存
保存路径根据需求自行修改
需要安装mysql数据库并执行以下代码
```sql
CREATE DATABASE `billing_details`
CREATE TABLE goods ( 
	gname VARCHAR(40)PRIMARY KEY, 
	gtype VARCHAR(20) NOT NULL, 
	ply DECIMAL(10, 4) NOT NULL, 
	width DECIMAL(10, 4) NOT NULL, 
	inv_price DECIMAL(10, 2) NOT NULL, 
	inv_qty_num  INT NOT NULL ,
	inv_qty_weight DECIMAL(10, 4) NOT NULL
	)COMMENT '商品信息'; 
CREATE TABLE supplier ( 
	sname VARCHAR(20)PRIMARY KEY 
	)COMMENT '供货商'; 
CREATE TABLE cg_name_price( 
	gname VARCHAR(20)NOT NULL , 
	cname VARCHAR(20)NOT NULL, 
	cg_price DECIMAL(10, 2)NOT NULL, 
	PRIMARY KEY (gname,cname), 
	FOREIGN KEY (gname) REFERENCES goods(gname) 
	)COMMENT '客户商品价格'; 
CREATE TABLE PO ( 
	id INT AUTO_INCREMENT PRIMARY KEY,
	sname VARCHAR(20)NOT NULL , 
	gname VARCHAR(20)NOT NULL, 
	p_price DECIMAL(10, 2)NOT NULL, 
	p_qty_num INT NOT NULL, 
	p_qty_weight DECIMAL(10, 4)NOT NULL,
	p_date DATE NOT NULL, 
	FOREIGN KEY (sname) REFERENCES supplier(sname), 
	FOREIGN KEY (gname) REFERENCES goods(gname) 
	)COMMENT '采购订单'; 
CREATE TABLE GO ( 
	id INT AUTO_INCREMENT PRIMARY KEY, 
	gname VARCHAR(20)NOT NULL , 
	cname VARCHAR(20)NOT NULL,
	g_price DECIMAL(10, 2)NOT NULL, 
	inv_price DECIMAL(10, 2) NOT NULL, 
	g_qty_num INT NOT NULL, 
	g_qty_weight DECIMAL(10, 4)NOT NULL, 
	g_date DATE NOT NULL, 
	FOREIGN KEY (gname,cname) REFERENCES cg_name_price(gname,cname), 
	FOREIGN KEY (gname) REFERENCES goods(gname)
	 )COMMENT '商品订单'; 
DROP TABLE `po`,`go`,`supplier`,`cg_name_price`,`goods`; 
```
