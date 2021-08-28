
-- Table: links
-- CREATE TABLE links (
--     link_id   INTEGER         PRIMARY KEY AUTO_INCREMENT,
--     link_name VARCHAR(512),
--     link_href TEXT,
--     link_desp TEXT,
--     link_rank INT( 10 )       DEFAULT 99,
--     link_ctms INT( 10 ),
--     link_utms INT( 10 )
-- );

--
-- -- Index: idx_linkRank_linkId
-- CREATE INDEX idx_linkRank_linkId ON links (
--     link_rank DESC,
--     link_id   DESC
-- );

INSERT INTO links (link_name, link_href, link_desp, link_ctms) VALUES ('品歌词', 'http://pingeci.com', '品歌词，品人生，搜索歌词，查询歌词', 1391144164);

