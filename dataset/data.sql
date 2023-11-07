

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
values ('РЕНИКСА', 'Реникса есть ни что иное, как ошибочное прочтение слова “чепуха”, воспринятого как латинского слова. О его употреблении рассказывал ещё Антон Павлович Чехов: “В какой-то семинарии учитель написал на сочинении “чепуха”, а ученик прочёл «реникса» — думал, по-латыни написано”. Но не всё, что на первый взгляд может показаться ненаучным фактом, в действительности ненаучно – многие известные факты тоже сначала казались неправдоподобными.

А сейчас мы проверим, насколько вы умеете отличать правду от ненаучного и видеть факты нескучные: в этом разделе мы собрали список как из научных фактов, так и из той самой “рениксы”.
');


insert into questions (in_group_id, question, group_id, answer_description)
values (1, 'ПАЛЕОНТОЛОГИЯ nn Птицы - это динозавры', 1, 'За последние 20 лет большинство палеонтологов пришли к консенсусу, что птиц можно считать динозаврами. Существуют ученые, кто не согласны, но данный момент таких меньшинство. Изменение представлений связано с большим количеством находок переходных форм (в Китае, например), кроме того сейчас понятно, что многие динозавры были пернатыми (находят много отпечатков перьев, раньше оставляли только кости и порой не обращали внимание на то, что рядом).'),
       (2, 'ФИЗИКА nn Тяжелая вода радиоактивна', 1, 'Да, тяжелая вода часто находится рядом с радиоактивными материалами (например, на атомных станциях). Но сама по себе не радиоактивна, потому что состоит из стабильного изотопа водорода – дейтерия.'),
       (3, 'АСТРОФИЗИКА nn В центре нашей галактики существует огромная черная дыра', 1, 'Да, по современным представлениям в центре нашей галактики находится сверхмассивная черная дыра Sgr A*. Еще любопытно, что по некоторым гипотезам черная дыра может быть в нашей солнечной системе.'),
       (4, 'ХИМИЯ nn Жидкая вода может существовать при отрицательной температуре', 1, 'Да, это правда. Существует целых две причины, по какой такое явление может существовать. Во-первых, мы не указали давление. Многие знают, что вода кипит при более высокой температуре при повышенном давлении, на этом основаны принцип действия актоклава и скороварки, тогда как в горах вода закипает при более низкой температуре. График зависимости агрегатного состояния вещества в зависимости от температуры и давления называется фазовая диаграмма. У воды она довольно необычная, лед менее плотный чем жидкая вода, поэтому при повышении давления он тает. Да вы и сами это вероятно наблюдали, под давлением лезвиев коньков лед тает и мы можем кататься. Таким образом чистая жидкая вода может существовать при температуре и -2 С, и -5 С, надо лишь увеличить давление.
Но и это не все. Оказывается, жидкая вода может существовать и при нормальном атмосферном давлении при температуре аж -48 градусов! Это явление носит название «переохлажденная вода». Вы можете провести эксперимент по получению переохлажденной воды в домашних условиях. Возьмите стакан с водой, и поставьте его в морозилку. Если все сделать аккуратно, то в какой-то момент вода будет еще жидкой, но при этом иметь температуру ниже 0 С. Но стоит бросить в нее льдинку — как она вся замерзнет.
'),
       (5, 'ТЕХНОЛОГИЯ nn Ядерную реакцию возможно провести в домашних условиях и никто не пострадает', 1, 'Реакцию синтеза ядер гелия из ионов изотопа водорода дейтерия провел американский школьник в своей домашней игровой комнате. Для этого он построил настоящий ускоритель, в котором ему удалось разогнать ионы дейтерия в электрическом поле и при ударе в мишень они образовали ядро гелия. Это самая настоящая ядерная реакция. Родители поддерживали юношу, но совершенно не боялись - никакой опасности не было.
Это специальный реактор – фузор.
Фузор Фарнсуорта — Хирша — устройство, сконструированное американским изобретателем Фило Т. Фарнсуортом для получения управляемой термоядерной реакции.В отличие от многих систем для получения управляемой термоядерной реакции, которые медленно нагревают плазму, помещенную в магнитную ловушку, в фузоре высокоэнергетические ионы напрямую впрыскиваются в область, где происходит термоядерная реакция. Гелия образуется совсем небольшое, но определяемое количество.
'),
       (6, 'НЕЙРОБИОЛОГИЯ nn Бабочка сохраняет память о том времени, когда она была личинкой', 1, 'В стадии куколки нейронные связи разрываются и перестраиваются настолько радикально, что память о том, как она была личинкой почти наверняка не сохраняется у бабочки.
«Трумэн и его сотрудники теперь узнали, насколько сильно метаморфоз перестраивает отдельные участки мозга. В недавнем исследовании, опубликованном в журнале eLife, они проследили за десятками нейронов в мозге плодовых мушек, проходящих через метаморфоз. Они обнаружили, что, в отличие от страдающего героя рассказа Франца Кафки «Метаморфозы», который однажды просыпается в виде чудовищного насекомого, взрослые насекомые, скорее всего, мало что помнят из своей личиночной жизни. Хотя многие личиночные нейроны в исследовании сохранились, та часть мозга насекомого, которую изучала группа Трумана, была кардинально перестроена. Эта перестройка нейронных связей отразила столь же резкие изменения в поведении насекомых, когда они превратились из ползающих голодных личинок в летающих взрослых особей, ищущих партнеров».
Получается, что при метаморфозисе бабочка фактически умирает и из той же ДНК возникает новое существо. Исследование 2023 года.
'),
       (7, 'АСТРОНОМИЯ nn Астероид можно назвать именем любимого питомца', 1, 'Астероидами (термин ввёл Уильям Гершель в 1802 году) или малыми планетами называются малые тела Солнечной системы (недостаточно большие, чтобы считаться планетой, но больше тридцати метров, меньшие объекты называют метеороидами), обращающиеся вокруг Солнца и не являющиеся кометами (для комет характерна газообразующая активность при приближении к Солнцу; при этом отдельные астероиды являются, по сути, «выродившимися», «потухшими» кометами. На текущий момент известно около 1 млн астероидов, и около 500 тысяч имеют постоянные номера (то есть имеют точные орбиты). Всеми названиями в космосе с 1922 года занимается Международный астрономический союз.
Первооткрыватель астероида имеет преимущественное право дать имя новой открытой им малой планете. Слово должно иметь не более 16 знаков, быть легко произносимым и не может быть прозвищем домашних животных. Кроме того, если малая планета называется именами полководцев или политиков, то со времени их жизни должно пройти не менее 100 лет.
'),
       (8, 'ИНЖЕНЕРИЯ nn Голос кита можно записать на компакт-диск', 1, 'Формат mp3 имеет максимальную частоту дискретизации 48 кГц, обычный CD - 44.1 кГц. Согласно теореме Котельникова (Найквиста) оцифровать без потерь можно аналоговый сигнал с частотой не более, чем половина от частоты дискретизации файла. Для mp3 это 24000 герц, для CD 22050. Этого достаточно для сохранения речи музыки и всего, что слышит человек, однако китообразные «поют» в гораздо более широком частотном диапазоне, например по данным [ Richardson, Greene, Malme, Thomson (1995). Marine Mammals and Noise. Academic Press. ISBN 978-0-12-588440-2.] до 31 кГц. Многие знают, что частота самых популярных CD/MP3 файлов 44.1 кГц и 16 бит. Почему именно 44,1? Теорема Котельникова (или теорема Найквиста — Шеннона, в русскоязычной литературе известная как Теорема Котельникова) — теорема о том, что если сигнал имеет ограниченный частотный спектр с максимальной частотой f, то он может быть восстановлен по его дискретным отсчетам частоты 2f.
Так как по существующим представлениям человеческое ухо способно различать звуки от 20 до 20 кГц, это могут быть музыка, голос и все шумы которые мы слышим. То есть все что лежит в этом диапазоне - это звук, выше и ниже - инфразвук и ультразвук. Согласно теореме Котельникова для исчерпывающего сохранения цифровой волны нам потребуется частота дискретизации не менее 40 кц. Формат GSM явно недостаточен: 8 кГц/2 = 4 кГц. А вот CD уже покрывает весь слышимый диапазон. Частота 96 кГц представляется избыточной; тем не менее в современных звуковых редакторах происходят преобразования цифрового сигнала, которые иногда сопровождаются искажениями и потерей точности передачи, поэтому для монтажа цифрового звука целесообразно иметь некоторый запас по частоте дискретизации.
');

insert into answers (question_id, answer_text, is_correct)
values (1, 'Правда',true),
       (1, 'Неправда',false),
       (2, 'Правда',false),
       (2, 'Неправда',true),
       (3, 'Правда',true),
       (3, 'Неправда',false),
       (4, 'Правда',true),
       (4, 'Неправда',false),
       (5, 'Правда',true),
       (5, 'Неправда',false),
       (6, 'Правда',false),
       (6, 'Неправда',true),
       (7, 'Правда',false),
       (7, 'Неправда',true),
       (8, 'Правда',false),
       (8, 'Неправда',true);

insert into question_groups (group_name, group_preview)
values ('РАЗВЕ ЭТО НАУЧНО?', 'По итогам первого раздела можно понять, что в мире куда больше неожиданных фактов в науке, нежели нам кажется. Но остаётся нераскрытым вопрос - а насколько представления о тех или иных терминах совпадают с научными?

	В этом разделе мы предлагаем оценить научность тех или иных терминов, основываясь на ваших знаниях и убеждениях. Нет смысла копаться в рамках лишь одной отрасли - вопросы к научности есть практически в каждой научной сфере, и ниже представлен ряд терминов, которые вам придётся разделить на научные и ненаучные.
');


insert into questions (in_group_id, question, group_id, answer_description)
values (1, 'ЛЕВИТАЦИЯ nn Тело может парить в условиях гравитации без опоры о воздух или любое другое физическое тело.', 2, 'Сегодня известна левитация сверхпроводников в магнитном поле, а за эксперимент с левитацией живой лягушки в сильном магнитном поле Андрей Гейм получил в 2000 году Шнобелевскую премию. Технология магнитной левитации сегодня используется для пассажирских поездов.'),
       (2, 'ТЕЛЕГОНИЯ nn Наследственность ребенка зависит не только от генов матери и отца, но и от генов предыдущих половых партнеров матери.', 2, 'На сегодня нет никаких научных данных, которые бы подтверждали передачу наследственного материала от предыдущих половых партнеров матери ребенку. Если, конечно, не считать таким «материалом» ВИЧ-инфекцию.'),
       (3, 'ПАНСПЕРМИЯ nn Источником жизни на Земле могли стать органические соединения, занесенные на нашу планету из космоса', 2, 'Глицин – это одна из основных аминокислот, которая входит в состав большинства белков. В 2016 году ученые сообщили об обнаружении глицина в газовом облаке кометы Чурюмова-Герасименко. Открытие было сделано с помощью прибора ROSINA, состоящего из двух масс-спектрометров и датчика давления.
Кроме глицина ученые обнаружили фосфор, который также является важным компонентом для возникновения жизни. Фосфаты, соединения содержащие фосфат-ион PO4−3, входят в состав ДНК, РНК и фосфолипидов, которые формируют клеточные мембраны. Это не исключительный случай. В 2009 году в ходе миссии Stardust аминокислота была найдена в хвосте кометы 81P/Вильда. А всего на кометах было найдено более полутора десятков разных органических соединений, включая спирты, амины, нитрилы, амиды и изоцианаты. И это только то, что достоверно существует. Гипотезы звучат еще более головокружительно. Химики из NASA доказали экспериментальным путем, что в космических условиях из простых молекул может образоваться витамин В3. Другой эксперимент показал, что вещество комет может содержать диамин-карбоксильные кислоты — строительные блоки пептидонуклеиновых кислот (ПНК). Есть предположение, что более простые и стойкие к действию высоких температур ПНК могли предшествовать молекулам РНК и ДНК в кодировании генетической информации у самых ранних организмов (гипотеза ПНК-мира), живших рядом с глубоководными вулканами. С учетом этого есть далеко не нулевая вероятность того, что кометы способствуют образованию первородного «бульона» в водоемах планет, которые подходят для поддержания жизни. А значит, гипотеза панспермии, согласно которой жизнь была занесена на Землю извне, может быть верна.
'),
       (4, 'ГОМЕОПАТИЯ nn При разбавлении нескольких граммов активного вещества водой в соотношении 1:100 200 раз (одно из стандартных разведений в гомеопатии, означающее, что исходное вещество разведено в соотношении 1:104°, в растворе остаются молекулы активного вещества.', 2, 'Количество молекул в одном моле вещества равно числу Авогадро 6,022140857(74)⋅1023. Столько молекул содержится в 12 граммах углерода. Разведение 1 моля «чистого» препарата до концентрации 1: 6,022⋅1023 (по классификации гомеопатов 12С) будет содержать только одну молекулу исходного вещества. Таким образом, вероятность того, что 1 моль разведения 13C содержит хотя бы одну молекулу исходного вещества, равна 1 %, для 14С 0,01 % и т. д., вероятность того, что эта молекула содержится в одной дозе препарата, — соответственно ещё меньше.
При приготовлении анаферона по утверждению производителей многократно разводятся антитела к белку гамма-интерферону. Если активное вещество разбавили водой в отношении 1:100 и процесс разбавления повторили 200 раз (200С) - а это довольно типичная процедура, используемая при изготовлении гомеопатических средств (например, того же анаферона), то наиболее вероятно, что никаких активных молекул в “лекарстве” просто нет: одна молекула на 100 000 000 таблеток. А есть в этом “лекарстве” только вода, молочный сахар и случайные примеси.
Как велик один моль? 6,022 . 1023 Приблизительное представление об этом гигантском числе мы сможем получить лишь на основе наглядного сравнения. Например, такого: представим себе, что все население земного шара 1990 года - примерно 6 миллиардов человек - приступило к подсчету этого количества атомов. Каждый считает по одному атому в секунду. За первую секунду сосчитали бы 6 . 109 атомов, за две секунды - 12 . 109 атомов и т. д. Сколько времени потребуется человечеству в 1990 году, чтобы сосчитать все атомы в одном моле? Ответ ошеломляет: около 3 200 000 лет!'),
       (5, 'АЛХИМИЯ nn Ртуть можно превратить в золото', 2, 'В 1940 году американские физики Шерр и Бэйнбридж доложили об успешных результатах: бомбардируя атомы ртути (80) быстрыми нейтронами, они получили золото (79). Другое дело, что изотопы имели массовые числа 198, 199 и 200. Таким образом, золото получили, но оно существовало короткий промежуток времени. Следовательно, современные приверженцы алхимии не имели повода ликовать, а эксперименты необходимо было продолжать. Далее было показано, что атомы ртути с массовыми числами 196 и 199 имеют больше всего шансов превратиться в золото - его единственный устойчивый изотоп золото-197. И после проведения реакции его действительно получили. 100 грамм ртути превратили в 35 мкг золота.');

insert into answers (question_id, answer_text, is_correct)
values (9, 'Правда',true),
       (9, 'Неправда',false),
       (10, 'Правда',false),
       (10, 'Неправда',true),
       (11, 'Правда',true),
       (11, 'Неправда',false),
       (12, 'Правда',false),
       (12, 'Неправда',true),
       (13, 'Правда',true),
       (13, 'Неправда',false);


insert into question_groups (group_name, group_preview)
values ('ВАША ВЕРСИЯ', 'Бесспорно, здравый смысл может вводить в заблуждение, и первые два раздела это наглядно подтвердили. Но у него есть неоценимые плюсы, которые с запасом перекрывают получающиеся нестыковки с реальностью - здравый смысл представляет мир как единое целое, и для формулирования гипотезы достаточно представить явление в общих чертах, как часть этого целого.

	Наш жизненный опыт включает себя не только здравый смысл, но и научные знания, которые мы получаем в течение всей жизни. Опираясь на весь свой жизненный опыт, вам предстоит ответить на ряд интересных вопросов из всех областей познания, где ваши познания о мире и ваш здравый смысл должны в некоем тандеме помочь найти правильный ответ из четырёх предложенных.
');

insert into questions (in_group_id, question, group_id)
values (1, 'ЭВОЛЮЦИЯ УСПОКОИТЕЛЬНЫХ nn Во все времена люди искали средства борьбы со стрессом и тревогой. В XX веке получили распространение 2 популярных класса противотревожных препаратов: барбитураты (напр. фенобарбитал) и бензодиазепины (напр., феназепам). К сожалению, при всей своей эффективности они вызывают тяжелую медикаментозную зависимость. Зависимость возникает в связи с тем, что оба класса препаратов воздействуют на рецепторы ГАМК, а это основной тормозный нейромедиатор в нашем мозге, сильное воздействие на них быстро изменяет чувствительность рецепторов по механизму обратной связи. Ученые давно пытаются разработать успокаивающие препараты, которые не вызывали бы зависимость. Было замечено, что препараты, открытые для лечения совсем других заболеваний — вызывают снотворное и успокоительное действие, и при этом практически не формируют зависимость. На их основе были разработаны новые противотревожные препараты. На рецепторы каких нейромедиаторов действуют эти препараты?', 3),
       (2, 'МЕТАМАТЕРИАЛЫ nn Метаматериалы встречаются и в живой природе, и это не такая большая редкость. Среди перечисленных объектов, только в одном случае природа «не воспользовалась» метаматериалами. В каком?', 3),
       (3, 'КРЕМЛЕВСКИЕ ЗВЕЗДЫ nn Кремлевские звезды, расположенные на башнях Московского кремля - это технологически сложные устройства. В центре каждой звезды находится мощный источник света. Он закрыт молочным стеклом, которое обеспечивает равномерное излучение вовне. А сама звезда состоит из специального стекла.
Что придает кремлевским звездам рубиновый цвет?', 3),
       (4, 'ИСТОРИЯ ТРОИ nn Стены легендарной Трои построили бог и герой - Посейдон и Геракл. Но ахейцы эти стены разрушили. На этом же месте был заново построен город, который называют Вторая Троя. Его стены построили люди. И построили из композитного материала.
Какой композит использовали для строительства стен 2500 лет назад троянцы?', 3),
       (5, 'УГЛЕРОДНЫЙ СЛЕД nn Предшественником термина «углеродный след» стала концепция «экологического следа», разработанная в 1990-х годах Уильямом Э. Рисом и Матисом Вакернагелем. Экологический след - это метод расчета размеров территории, необходимой для удовлетворения текущих потребностей человека и поглощения отходов, связанных с этим потреблением.
Углеродный след - это индикатор, который оценивает лишь общее количество выбросов углекислого газа, связанное с конкретным видом деятельности или потреблением ресурсов. Как вы думаете, какой из видов энергетики оставляет наименьший углеродный след при выработке 1 ГВт электроэнергии?',3),
       (6, 'ОПТИЧЕСКИЙ ПИНЦЕТ nn При работе с наноразмерными объектами их можно захватывать лазерным излучением.
Устройство, реализующее этот метод, называется оптическим пинцетом (Нобелевская премия 2018 года по физике Артуру Эшкину). Сколько минимум нужно источников лазерного излучения, чтобы захватить одну молекулу?',3),
       (7, 'ТЕКТОНИКА ПЛИТ nn Сколько континентов останется на Земле через 200 миллионов лет?', 3),
       (8, 'И ОПЯТЬ О ДИНОЗАВРАХ
Наши знания о динозаврах довольно сильно продвинулись за последние годы. Какое из утверждений на ваш взгляд на текущий момент является неправильным?',3);

insert into answers (question_id, answer_text, is_correct)
values (14, 'Дофамина',false),
       (14, 'Гистамина',true),
       (14, 'Серотонина',false),
       (14, 'Норадреналина',false),

       (15, 'Крылья бабочки Morpho',false),
       (15, 'Крылья моли',false),
       (15, 'Кожа хамелеона',false),
       (15, 'Лапки геккона',true),

       (16, 'Напыление из драгоценного рубина',false),
       (16, 'Добавки меди',false),
       (16, 'Добавки золота',true),
       (16, 'Силикатная краска с добавлением серебра',false),

       (17, 'Армированный мрамор',false),
       (17, 'Железобетонные блоки',false),
       (17, 'Саманный кирпич',true),
       (17, 'Многослойная фанера',false),

       (18, 'Ископаемая энергетика',false),
       (18, 'Атомная энергетика',true),
       (18, 'Ветроэнергетика',false),
       (18, 'Солнечная энергетика',false),

       (19, 'Один',true),
       (19, 'Два',false),
       (19, 'Три',false),
       (19, 'Более трех',false),

       (20, 'Один суперконтинент',true),
       (20, 'По одному в каждом полушарии',false),
       (20, 'Ни одного: все плиты растрескаются на острова',false),
       (20, 'Столько же, сколько и сегодня',false),

       (21, 'Некоторые динозавры вероятно были теплокровными',false),
       (21, 'Нам удалось секвенировать ДНК динозавров',true),
       (21, 'Существовали динозавры с яркими пушистыми хвостами',false),
       (21, 'Динозавров можно найти под Московским Кремлем',false);

insert into question_groups (group_name, group_preview)
values ('МАСШТАБ ЯВЛЕНИЙ', 'Наш мир безграничен, и многие его явления просто поражают воображение. Но не стоит забывать, что оценка этих явлений, даже самая приблизительная - уже половина успеха, ведь в науке без чисел, без оценок и приближений нельзя добиться никакого прогресса. Сейчас вам предстоит столкнуться с несколькими явлениями, которые могут удивить неподготовленного наблюдателя, и их даже приблизительная оценка может привести вас в шок. Или же нет?

Так давайте же выясним, насколько ваши представления об окружающем нас мире сходны с тем, что происходит на самом деле. Как и в предыдущем разделе, у вас есть 4 варианта ответа, среди которых корректным является только один - вашей задачей является ответить, насколько масштабны те или иные явления прошлого и настоящего, на макро- и микроуровне.
');

insert into questions (in_group_id, question, group_id)
values (1, 'ЭТАЛОН КИЛОГРАММА nn После того, как в 1889 году был изготовлен эталон килограмма, он сохранялся в Севре (коммуна в юго-западных предместьях Парижа) в Международном бюро мер и весов. Были также изготовлены его копии, которые хранятся в национальных метрологических учреждениях по всему миру. После сверки эталонов было обнаружено, что их расхождение накапливается и составляет 50 мкг за 100 лет. Что стало причиной расхождения эталонов?', 4),
       (2, 'КАК ЧАСТО НАДО ЗАПРАВЛЯТЬ АТОМНЫЙ ЛЕДОКОЛ? nn Ледоколы - это особый класс кораблей, которые предназначены для преодоления толстых льдов. Они активно применяются в разных сферах: сопровождают торговые суда, используются для поддержки исследовательских программ, проводимых в полярных регионах, и даже могут принимать на своём борту туристов. Чтобы ломать лед, такие корабли должны быть мощными, широкими и тяжелыми, а наиболее эффективный их вид - это атомный. Как и любому транспортному средству, ему необходимо топливо и заправка. Как часто надо заправлять современный атомный ледокол?', 4),
       (3, 'ВЫСОКОТЕМПЕРАТУРНАЯ СВЕРХПРОВОДИМОСТЬ nn Сверхпроводимостью называется свойство материала при температуре ниже критической переходить в состояние, когда его сопротивление почти мгновенно падает до нуля. Это явление было открыто в начале XX века для металлической ртути: она становится сверхпроводником при температуре -269 °С. Если бы отыскался материал, критическая температура которого достаточно высокая, например, комнатная, и он переходит в сверхпроводящее состояние при нормальном давлении т это привело бы к невероятной экономии электроэнергии, которая сейчас теряется при электрическом сопротивлении. Поиски таких материалов — это Святой Грааль физики конденсированных состояний.
Какова максимальная температура для которой на сегодняшний день получены материалы, переходящие в сверхпроводящее состояние (только подтвержденные результаты)?', 4),
       (4, 'БУТЫЛОЧНОЕ ГОРЛЫШКО В ПОПУЛЯЦИИ ЧЕЛОВЕКА nn Согласно одной изт последних работ генетиков, недавно опубликованной в журнале Science, около 900 тыс. лет назад в истории человечества едва не случилась катастрофа. Предки человека почти вымерли. Численность половозрелых особей в популяции, которая в дальнейшем стала прародителем всех ныне живущих на планете людей, резко сократилась примерно до...', 4),
       (5, 'РАЗМЕР ЯДРА АТОМА nn Если мы увеличим атом примерно до размеров футбольного поля (около 100 метров в поперечнике), то какой размер будет у атомного ядра?', 4),
       (6, 'ВЫСОКОТЕМПЕРАТУРНАЯ СВЕРХПРОВОДИМОСТЬ nn Сверхпроводимостью называется свойство материала при температуре ниже критической переходить в состояние, когда его сопротивление почти мгновенно падает до нуля. Это явление было открыто в начале XX века для металлической ртути: она становится сверхпроводником при температуре -269 °С. Если бы отыскался материал, критическая температура которого достаточно высокая, например, комнатная, и он переходит в сверхпроводящее состояние при нормальном давлении т это привело бы к невероятной экономии электроэнергии, которая сейчас теряется при электрическом сопротивлении. Поиски таких материалов — это Святой Грааль физики конденсированных состояний. Какова максимальная температура для которой на сегодняшний день получены материалы, переходящие в сверхпроводящее состояние (только подтвержденные результаты)?', 4);

insert into answers (question_id, answer_text, is_correct)
values (22, 'Космические лучи',true),
       (22, 'Солнечный ветер',false),
       (22, 'Радиоактивный распад',false),
       (22, 'Нарушение условий хранения',false),

       (23, 'Каждый рейс',false),
       (23, 'Каждый сезон, то есть раз в год',false),
       (23, 'Раз в несколько лет',false),
       (23, 'Один раз за время эксплуатации',true),

       (24, '127 °C',false),
       (24, '15 °C',false),
       (24, '-13 °C',true),
       (24, '-181 °C',false),

       (25, '150',false),
       (25, '1500',true),
       (25, '15 000',false),
       (25, '150 000',false),

       (26, 'Как диаметр центрального круга (10 м)',false),
       (26, 'Как диаметр футбольного мяча (35 см)',false),
       (26, 'Как диаметр ягоды вишни (1 см)',true),
       (26, 'Не больше пылинки (менее 1 мм)',false),

       (27, 'Примерно 1 литр',false),
       (27, 'Примерно 10 литров',false),
       (27, 'Примерно 100 литров',false),
       (27, 'Примерно 500 литров',true);





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