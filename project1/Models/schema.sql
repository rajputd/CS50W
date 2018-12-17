CREATE TABLE users (
  user_id serial primary key,
  username varchar(20),
  password varchar(20)
);

CREATE TABLE books (
  book_id serial primary key,
  isbn char(10),
  title varchar(30),
  author varchar(30),
  year int
);

CREATE TABLE reviews (
  rating int,
  review_content text,
  reviewer_id int,
  book_id int,
  primary key (reviewer_id, book_id)
);
