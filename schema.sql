CREATE table user(
     id int primary key,
     username text not null,
     password text not null,
     teamname text not null
);

CREATE table pitcher_data(
       data_id int primary key,
       pitcher_name text not null,
       day text not null,
       pitch_type text not null,
       pitch_speed real not null,
       rotations int not null,
       r_efficiency int not null,
       v_change real not null,
       h_change real not null,
       id int not null
);
