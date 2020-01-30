create table users(
    `id` VARCHAR(32) PRIMARY KEY,
    `follower_total` INT UNSIGNED DEFAULT 0,
    `url` TEXT,
    `icon` TEXT,
    `bio` TEXT,
    `checked` BOOLEAN DEFAULT 0
);
insert into users (id,follower_total, url, icon) values ('Chikirin', 4147, 'https://chikirin.hatenablog.com/', 'https://cdn.profile-image.st-hatena.com/users/Chikirin/profile.png');

create table follows(
    `follow_to` VARCHAR(32),
    `follow_by` VARCHAR(32),
    FOREIGN KEY (follow_to) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (follow_by) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE to_and_by(follow_to, follow_by)
);

select users.id, users.url, users.follower_total, count(follows.follow_to) from users inner join follows on follows.follow_to = users.id group by users.id, users.follower_total,users.url order by follower_total DESC limit 100;

SELECT id, icon, url,follower_total FROM users
    INNER JOIN follows ON users.id = follows.follow_by
        WHERE follows.follow_to = 'Chikirin' ORDER BY follower_total DESC LIMIT 10;

        SELECT id, icon, url,follower_total FROM users
    INNER JOIN follows ON users.id = follows.follow_to
        WHERE follows.follow_by = 'mennou' ORDER BY follower_total DESC LIMIT 10;