# Task 1
use dst;
create table dst2studentaccount (
    student_id      serial          primary key,
    first_name      varchar(50)     unique,
    last_name       varchar(50),
    email           varchar(355)    unique,
    create_on       timestamp,
    last_login      timestamp
);

# Create new tables
CREATE TABLE customer (
    customer_name       char(20),
    customer_street     char(30),
    customer_city       char(30),
    PRIMARY KEY(customer_name)
);
CREATE TABLE branch (
    branch_name     char(15),
    branch_city     char(30),
    assets          numeric(12,2),
    PRIMARY KEY (branch_name)
);
CREATE TABLE account (
    account_number      char(10),
    branch_name         char(15),
    balance             integer,
    PRIMARY KEY (account_number),
    FOREIGN KEY (branch_name) REFERENCES branch(branch_name)
);
CREATE TABLE depositor (
    customer_name       char(20),
    account_number      char(10),
    PRIMARY KEY (customer_name, account_number),
    FOREIGN KEY (account_number) REFERENCES account(account_number),
    FOREIGN KEY (customer_name) REFERENCES customer(customer_name)
);

# Task 2
INSERT INTO customer (customer_name, customer_street, customer_city)
VALUES ('Smith', 'First', 'Hangzhou');
INSERT INTO branch (branch_name, branch_city, assets)
VALUES ('CITIHZ', 'Hangzhou', 1000000.00);
INSERT INTO account (account_number, branch_name, balance)
VALUES ('2', 'CITIHZ', 1000.00);
INSERT INTO depositor (customer_name, account_number)
VALUES ('Smith', '2');

# Task3
create database if not exists spjdst2;
use spjdst2;
CREATE TABLE Supplier(
    supplier_number	int,
    supplier_name	varchar(30),
    supplier_status	boolean,
    supplier_city	varchar(30),
    PRIMARY KEY(supplier_number)
);
CREATE TABLE Part (
    part_number	int,
    part_name	varchar(20),
    part_color	varchar(30),
    part_weight	decimal(20,2),
    part_city	varchar(10),
    PRIMARY KEY (part_number)
);
CREATE TABLE Project(
    project_number	int,
	project_name	varchar(15),
	project_cit	    int,
	PRIMARY KEY (project_number)
);

CREATE TABLE SPJ(
    supplier_number	int,
	part_number	    int,
	project_number	int,
	quantity	    int,
	PRIMARY KEY (supplier_number, part_number, project_number),
	FOREIGN KEY (supplier_number) REFERENCES    Supplier(supplier_number),
	FOREIGN KEY (part_number) REFERENCES        Part(part_number),
    FOREIGN KEY (project_number) REFERENCES     Project(project_number)
);

# Task 4
set global log_bin_trust_function_creators = TRUE;
delimiter //
create function RMB_to_USD (x double)
returns double
begin
    return x/7;
end //
delimiter ;
select RMB_to_USD(100);

# Task 5
use dvdrental;
delimiter //
create procedure get_film_by_pattern (x varchar(50))
BEGIN
    select * from film where title LIKE x;
end //
delimiter ;

call get_film_by_pattern('e%');

# Task 6
delimiter //
CREATE PROCEDURE compare_date(a date, b date)
BEGIN
IF a>b THEN select 'date1 is later than date2' as result;
ELSEIF a=b THEN select 'date1 equals date2' as result;
ELSE select 'date1 is earlier than date2' as result;
END IF;
END//
delimiter ;

CALL compare_date('2021-9-20', '2021-10-20');
CALL compare_date('2021-11-20', '2021-10-20');

# Example for loop
delimiter //
create procedure sum_loop (N int)
begin
    declare s int default 0;
    declare i int default 1;
    lp : loop
        set s = s+i;
        set i = i+1;
        if i>N then
            select i as 'added', s as 'result';
            leave lp;
        end if;
    end loop lp;
end//
delimiter ;

call sum_loop(100);

# Task 7
delimiter /
create procedure product_loop (N int)
begin
    declare result int default 1;
    declare ind int default 1;
    wyxsg: loop
        set result = result * ind;
        set ind = ind + 1;
        if ind > N then
            select result;
            leave wyxsg;
        end if ;
    end loop wyxsg;
end /
delimiter ;

call product_loop(5);