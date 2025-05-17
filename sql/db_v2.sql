create table categories
(
    id          int auto_increment
        primary key,
    name        varchar(45)          not null,
    description varchar(255)         null,
    hidden      tinyint(1) default 0 not null,
    constraint name_UNIQUE
        unique (name)
);

create table users
(
    id            int auto_increment
        primary key,
    username      varchar(45)               not null,
    password      varchar(255)              not null,
    email         varchar(45)               not null,
    birthday      date                      not null,
    avatar        tinytext                  null,
    admin         tinyint default 0         not null,
    creation_date date    default curdate() null,
    constraint email_UNIQUE
        unique (email),
    constraint username_UNIQUE
        unique (username)
);

create table category_permissions
(
    id          int auto_increment,
    type        tinyint default 0 not null,
    category_id int               not null,
    user_id     int               not null,
    primary key (id, category_id, user_id),
    constraint fk_category_permissions_categories1
        foreign key (category_id) references categories (id)
            on delete cascade,
    constraint fk_category_permissions_users1
        foreign key (user_id) references users (id)
            on delete cascade
);

create index fk_category_permissions_categories1_idx
    on category_permissions (category_id);

create index fk_category_permissions_users1_idx
    on category_permissions (user_id);

create table conversations
(
    id           int auto_increment,
    date         datetime default current_timestamp() not null,
    initiator_id int                                  not null,
    receiver_id  int                                  not null,
    seen         int      default 0                   not null,
    primary key (id, initiator_id, receiver_id),
    constraint fk_conversations_users1
        foreign key (initiator_id) references users (id)
            on delete cascade,
    constraint fk_conversations_users2
        foreign key (receiver_id) references users (id)
            on delete cascade
);

create index fk_conversations_users1_idx
    on conversations (initiator_id);

create index fk_conversations_users2_idx
    on conversations (receiver_id);

create table messages
(
    id              int auto_increment,
    content         varchar(255)                         not null,
    date            datetime default current_timestamp() not null,
    conversation_id int                                  not null,
    sender_id       int                                  not null,
    receiver_id     int                                  not null,
    primary key (id, conversation_id, sender_id),
    constraint fk_messages_conversations1
        foreign key (conversation_id) references conversations (id)
            on delete cascade,
    constraint fk_messages_users1
        foreign key (sender_id) references users (id)
            on delete cascade,
    constraint fk_messages_users2
        foreign key (receiver_id) references users (id)
            on delete cascade
);

create index fk_messages_conversations1_idx
    on messages (conversation_id);

create index fk_messages_users1_idx
    on messages (sender_id);

create index fk_messages_users2_idx
    on messages (receiver_id);

create table topics
(
    id          int auto_increment,
    name        varchar(45)                  not null,
    content     mediumtext                   not null,
    date        date       default curdate() not null,
    category_id int                          not null,
    user_id     int                          not null,
    locked      tinyint(1) default 0         null,
    primary key (id, category_id, user_id),
    constraint fk_topics_categories
        foreign key (category_id) references categories (id)
            on delete cascade,
    constraint fk_topics_users1
        foreign key (user_id) references users (id)
            on delete cascade
);

create table replies
(
    id         int auto_increment,
    content    text                      not null,
    date       date    default curdate() not null,
    topic_id   int                       not null,
    user_id    int                       not null,
    best_reply tinyint default 0         null,
    primary key (id, topic_id, user_id),
    constraint fk_replies_topics1
        foreign key (topic_id) references topics (id)
            on delete cascade,
    constraint fk_replies_users1
        foreign key (user_id) references users (id)
            on delete cascade
);

create index fk_replies_topics1_idx
    on replies (topic_id);

create index fk_replies_users1_idx
    on replies (user_id);

create index fk_topics_categories_idx
    on topics (category_id);

create index fk_topics_users1_idx
    on topics (user_id);

create table votes
(
    id       int auto_increment,
    type     tinyint not null,
    reply_id int     not null,
    user_id  int     not null,
    primary key (id, reply_id, user_id),
    constraint fk_votes_replies1
        foreign key (reply_id) references replies (id)
            on delete cascade,
    constraint fk_votes_users1
        foreign key (user_id) references users (id)
            on delete cascade
);

create index fk_votes_replies1_idx
    on votes (reply_id);

create index fk_votes_users1_idx
    on votes (user_id);

