--
-- Data dump for table `aula_fisica`
--

INSERT INTO `aula_fisica` (`id_aula`, `capienza`) VALUES
(1, 2),
(2, 2);

--
-- Data dump for table `corso`
--

INSERT INTO `corso` (`id_corso`, `nome_corso`) VALUES
(1, 'Matematica'),
(2, 'Informatica');

-- --------------------------------------------------------

--
-- Data dump for table `data_lezione`
--

INSERT INTO `data_lezione` (`id_data`, `G_settimana`, `ora`, `id_lezione`, `id_aula`) VALUES
(1, 'Lunedi', '09:00:00', 2, 1),
(2, 'Lunedi', '11:00:00', 3, 1),
(3, 'Martedi', '09:00:00', 2, 2),
(4, 'Martedi', '09:00:00', 3, 2),
(5, 'Mercoledi', '09:00:00', 2, 1),
(6, 'Mercoledi', '09:00:00', 3, 2),
(7, 'Giovedi', '09:00:00', 1, 1),
(8, 'Giovedi', '11:00:00', 2, 2),
(9, 'Venerdi', '09:00:00', 3, 2),
(10, 'Venerdi', '11:00:00', 2, 2);

-- --------------------------------------------------------

--
-- Data dump for table `docenti`
--

INSERT INTO `docenti` (`id_docente`, `nome`, `cognome`, `email`) VALUES
(1, 'Franco', 'Gemelli', 'franco.gemelli@unipg.it'),
(2, 'Lorenzo', 'Magna', 'lorenzo.magna@unpg.it'),
(3, 'Nicola', 'Minotti', 'nicola.minotti@unipg.it');

-- --------------------------------------------------------

-- 
-- Data dump for table `lezioni`
--

INSERT INTO `lezioni` (`id_lezione`, `nome_lezione`, `descrizione`, `id_corso`, `id_docente`) VALUES
(1, 'Statistica Matematica', 'La Statistica Matematica è una disciplina che si occupa dell\'analisi, interpretazione e presentazione dei dati utilizzando modelli matematici e teorie probabilistiche. Questa materia è fondamentale per comprendere come raccogliere, organizzare e analizzar', 1, 3),
(2, 'Matematica Finanziaria', 'La Matematica Finanziaria è una disciplina che applica principi matematici e statistici per risolvere problemi finanziari. Essa si occupa dello studio dei mercati finanziari, della valutazione degli investimenti e della gestione del rischio. L\'obiettivo p', 1, 1),
(3, 'Programmazione Procedurale', 'La Programmazione Procedurale è un paradigma di programmazione che si basa sulla concettualizzazione dei programmi come una serie di procedure o funzioni che operano su dati. Questo approccio enfatizza l\'uso di procedure (o subroutine), che sono blocchi d', 2, 2);

-- --------------------------------------------------------

--
-- Data dump for table `studente`
--

INSERT INTO `studente` (`matricola`, `nome`, `cognome`, `email`, `password`) VALUES
(355545, 'Giuseppe', 'Gallo', 'giuseppe.gallo@studenti.unipg.it', 'studente22@'),
(355644, 'Mario', 'Gialli', 'mario.gialli@studenti.unipg.it', 'saetta144@'),
(367484, 'Carlo', 'Rossi', 'carlo.rossi@studenti.unipg.it', 'calamaro13?');

-- --------------------------------------------------------

--
-- Data dump for table `studente`
--

INSERT INTO `studente` (`matricola`, `nome`, `cognome`, `email`, `password`) VALUES
(355545, 'Giuseppe', 'Gallo', 'giuseppe.gallo@studenti.unipg.it', 'studente22@'),
(355644, 'Mario', 'Gialli', 'mario.gialli@studenti.unipg.it', 'saetta144@'),
(367484, 'Carlo', 'Rossi', 'carlo.rossi@studenti.unipg.it', 'calamaro13?');