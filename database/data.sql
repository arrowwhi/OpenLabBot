

CREATE TABLE question_groups (
    id SERIAL PRIMARY KEY,
    group_name VARCHAR NOT NULL,
    group_preview VARCHAR
);

CREATE TABLE users (
    tg_id INT PRIMARY KEY,
    name VARCHAR NOT NULL,
    age INT NOT NULL,
    gender VARCHAR,
    education VARCHAR NOT NULL,
    edu_sector VARCHAR,
    create_date TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    in_group_id INT,
    question VARCHAR,
    group_id INT REFERENCES question_groups(id),
    answer_description TEXT
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INT REFERENCES questions(id),
    answer_text VARCHAR,
    is_correct BOOLEAN
);

CREATE TABLE users_answers (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(tg_id),
    question_id INT REFERENCES questions(id),
    answer_id INT REFERENCES answers(id),
    is_correct BOOLEAN
);

CREATE TABLE user_current_question (
    tg_id BIGINT PRIMARY KEY,
    current_group INT REFERENCES question_groups(id) DEFAULT 1,
    current_question INT DEFAULT 1,
    is_completed BOOLEAN DEFAULT FALSE,
    final_score INT DEFAULT 0
);


insert into question_groups (group_name, group_preview)
values ('Реникса', 'В этом разделе мы собрали список надежных фактов и наукоподобной чепухи - рениксы. Проверьте, уверенно ли вы их различаете.');


insert into questions (in_group_id, question, group_id, answer_description)
values (1, 'ПАЛЕОНТОЛОГИЯ nn Птицы - это динозавры', 1, 'desc1'),
       (2, 'ФИЗИКА nn Тяжелая вода радиоактивна', 1, 'desc2'),
       (3, 'АСТРОФИЗИКА nn В центре нашей галактики существует огромная черная дырв', 1, 'desc3'),
       (4, 'ХИМИЯ nn Жидкая вода может существовать при отрицательной температуре', 1, 'desc4'),
       (5, 'ТЕХНОЛОГИЯ nn Ядерную реакцию возможно провести в домашних условиях и никто не пострадает', 1, 'desc5'),
       (6, 'НЕЙРОБИОЛОГИЯ nn Бабочка сохраняет память о том времени, когда она была личинкой', 1, 'desc6'),
       (7, 'АСТРОНОМИЯ nn Астероид можно назвать именем любимого питомца', 1, 'desc7'),
       (8, 'ИНЖЕНЕРИЯ nn Голос кита можно записать на компакт-диск', 1, 'desc8');

insert into answers (question_id, answer_text, is_correct)
values (1, 'Правда',false),
       (1, 'Неправда',true),
       (2, 'Правда',false),
       (2, 'Неправда',true),
       (3, 'Правда',false),
       (3, 'Неправда',true),
       (4, 'Правда',false),
       (4, 'Неправда',true),
       (5, 'Правда',false),
       (5, 'Неправда',true),
       (6, 'Правда',false),
       (6, 'Неправда',true),
       (7, 'Правда',false),
       (7, 'Неправда',true),
       (8, 'Правда',false),
       (8, 'Неправда',true);

insert into question_groups (group_name, group_preview)
values ('РАЗВЕ ЭТО НАУЧНО?', 'Проверье, насколько ваши представления об этих терминах совпадают с научными.');


insert into questions (in_group_id, question, group_id)
values (1, 'ЛЕВИТАЦИЯ nn Тело может парить в условиях гравитации без опоры о воздух или любое другое физическое тело.', 2),
       (2, 'ТЕЛЕГОНИЯ nn Наследственность ребенка зависит не только от генов матери и отца, но и от генов предыдущих половых партнеров матери.', 2),
       (3, 'ПАНСПЕРМИЯ nn Источником жизни на Земле могли стать органические соединения, занесенные на нашу планету из космоса', 2),
       (4, 'ГОМЕОПАТИЯ nn При разбавлении нескольких граммов активного вещества водой в соотношении 1:100 200 раз (одно из стандартных разведений в гомеопатии, означающее, что исходное вещество разведено в соотношении 1:104°, в растворе остаются молекулы активного вещества.', 2),
       (5, 'АЛХИМИЯ nn Ртуть можно превратить в золото', 2);

insert into answers (question_id, answer_text, is_correct)
values (9, 'Правда',false),
       (9, 'Неправда',true),
       (10, 'Правда',false),
       (10, 'Неправда',true),
       (11, 'Правда',false),
       (11, 'Неправда',true),
       (12, 'Правда',false),
       (12, 'Неправда',true),
       (13, 'Правда',false),
       (13, 'Неправда',true);


CREATE FUNCTION check_duplicates()
RETURNS TRIGGER
AS
$$
BEGIN
  -- Проверяем, имеется ли в таблице строка с такими же комбинациями части колонок
  IF EXISTS (
    SELECT 1
    FROM users_answers
    WHERE
      -- Указываем части колонок, по которым будем проверять наличие дубликатов
      user_id = NEW.user_id AND
      question_id = NEW.question_id
  ) THEN
    RAISE EXCEPTION 'Дубликат строки!';
  END IF;
  RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER on_insert
BEFORE INSERT
ON users_answers
FOR EACH ROW
EXECUTE PROCEDURE check_duplicates();