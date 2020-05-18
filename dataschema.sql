CREATE table pitcher_data(
       data_id int not null PRIMARY KEY,
       pitcher_name text not null,
       day text not null,
       pitch_type text not null,
       pitch_speed real not null,
       rotations real not null,
       r_efficiency real not null,
       v_change real not null,
       h_change real not null
)
