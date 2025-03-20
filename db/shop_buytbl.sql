CREATE TABLE buy1tbl (
	idnum number(8) NOT NULL,
	userid char(8) NOT NULL,
	prodname nchar(8) NOT NULL,
	groupname nchar(4),
	price number(8) NOT NULL,
	amount number(3) NOT NULL,
	usertbl_userid char(8) NOT null
);

ALTER TABLE BUY1TBL ADD CONSTRAINT buy1tbl_pk PRIMARY KEY (idnum);

ALTER TABLE BUY1TBL ADD CONSTRAINT buy1tbl_user1tbl_fk FOREIGN KEY (usertbl_userid)
REFERENCES user1tbl(userid);
