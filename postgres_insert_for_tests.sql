begin transaction;

insert into "_Production".country
VALUES
(1,'test',now());

insert into "_Production".state
VALUES
 (1,'test','t',1,now());
 
insert into "_Production".county
VALUES
(1, 'test', 1 , now());

insert into "_Production".city
VALUES
(1,'test',1,1,now());

insert into "_Production".paymentlevel
VALUES
(1,'test','test',now());

commit transaction;