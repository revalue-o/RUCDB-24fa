-- 学生
create table student
(
    -- 学生id(学工号)
	sno char(10) primary key,

    -- 密码
	spasswd varchar(64),

    -- 学生姓名
	sname varchar(16)
);

create table assignment
(
    -- 作业id
    ano serial primary key,

    -- 作业名称
    aname varchar(64),

    -- 截止时间
    adeadline timestamp,

    -- 作业简介
    aprofile varchar(1024),

    -- 文件路径
    afilepath varchar(128)
);

create table course
(
    -- 课程id
    courseno serial primary key,

    -- 课程名称
    coursename varchar(32)
);

create table class
(
    -- 教学班id
    cno serial primary key,

    -- 教学班名
    cname varchar(32),

    -- 开课学期
    csemester char(5),

    -- 对应课程
    courseno serial,

    foreign key (courseno) references course(courseno)
);

create table teacher
(
    -- 教师id(学工号)
	tno char(10) primary key,

    -- 密码
	tpasswd varchar(64),

    -- 学生姓名
	tname varchar(16)
);


create table handout
(
    -- 课件id
    hno serial primary key,

    -- 课件名称
    hname varchar(64),

    hfilepath varchar(128)
);

create table submit_assignment
(
    -- 学生id(学工号)
	sno char(10),

    -- 作业id
    ano serial,

    -- 提交时间
    submit_time timestamp,

    -- 是否超时
    is_over_time boolean,

    -- 文件路径
    submit_filepath varchar(128),

    primary key (sno, ano),
    foreign key (sno) references student(sno),
    foreign key (ano) references assignment(ano)
);

create table post_assignment
(
    -- 教学班id
    cno serial,

    -- 作业id
    ano serial,

    -- 教师id(学工号)
	tno char(10),

    -- 布置时间
    post_assignment_time timestamp,

    primary key (cno, ano),
    foreign key (cno) references class (cno),
    foreign key (ano) references assignment (ano),
    foreign key (tno) references teacher (tno)
);

create table post_handout
(
    -- 教学班id
    cno serial,

    -- 课件id
    hno serial,

    -- 教师id(学工号)
	tno char(10),

    -- 布置时间
    post_handout_time timestamp,

    primary key (cno, hno),
    foreign key (cno) references class (cno),
    foreign key (hno) references handout (hno),
    foreign key (tno) references teacher (tno)
);

create table attend_class
(
    -- 学生id(学工号)
	sno char(10),

    -- 教学班id
    cno serial,

    primary key (sno, cno),
    foreign key (sno) references student (sno),
    foreign key (cno) references class (cno)
);

create table teach_class
(
    -- 教师id(学工号)
	tno char(10),

    -- 教学班id
    cno serial,

    -- 是否为助教
    is_ta boolean,

    primary key (tno, cno),
    foreign key (tno) references teacher (tno),
    foreign key (cno) references class (cno)
);

