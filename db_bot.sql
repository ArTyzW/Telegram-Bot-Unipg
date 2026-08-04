-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Created on: Jul 04, 2024 at 19:24
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";




--
-- Database: `telebot`
--

-- --------------------------------------------------------

--
-- Structure of table `aula_fisica`
--

CREATE TABLE `aula_fisica` (
  `id_aula` int(11) NOT NULL,
  `capienza` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Structure of table `corso`
--

CREATE TABLE `corso` (
  `id_corso` int(11) NOT NULL,
  `nome_corso` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



--
-- Structure of table `data_lezione`
--

CREATE TABLE `data_lezione` (
  `id_data` int(11) NOT NULL,
  `G_settimana` varchar(25) NOT NULL,
  `ora` time NOT NULL,
  `id_lezione` int(10) NOT NULL,
  `id_aula` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



--
-- Structure of table `docenti`
--

CREATE TABLE `docenti` (
  `id_docente` int(11) NOT NULL,
  `nome` varchar(25) NOT NULL,
  `cognome` varchar(25) NOT NULL,
  `email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



--
-- Structure of table `lezioni`
--

CREATE TABLE `lezioni` (
  `id_lezione` int(10) NOT NULL,
  `nome_lezione` varchar(255) NOT NULL,
  `descrizione` varchar(300) NOT NULL,
  `id_corso` int(10) NOT NULL,
  `id_docente` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



--
-- Structure of table `prenotazioni`
--

CREATE TABLE `prenotazioni` (
  `id_prenotazione` int(10) NOT NULL,
  `matricola` int(6) NOT NULL,
  `id_data` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure of table `studente`
--

CREATE TABLE `studente` (
  `matricola` int(6) NOT NULL,
  `nome` varchar(25) NOT NULL,
  `cognome` varchar(25) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for table `aula_fisica`
--
ALTER TABLE `aula_fisica`
  ADD PRIMARY KEY (`id_aula`);

--
-- Indexes for table `corso`
--
ALTER TABLE `corso`
  ADD PRIMARY KEY (`id_corso`);

--
-- Indexes for table `data_lezione`
--
ALTER TABLE `data_lezione`
  ADD PRIMARY KEY (`id_data`),
  ADD KEY `FK_DATALEZIONE_LEZIONE` (`id_lezione`),
  ADD KEY `FK_FATALEZIONI_AULAFISICA` (`id_aula`);

--
-- Indexes for table `docenti`
--
ALTER TABLE `docenti`
  ADD PRIMARY KEY (`id_docente`);

--
-- Indexes for table `lezioni`
--
ALTER TABLE `lezioni`
  ADD PRIMARY KEY (`id_lezione`),
  ADD KEY `FK_LEZIONI_DOCENTE` (`id_docente`),
  ADD KEY `FK_LEZIONI_CORSO` (`id_corso`);

--
-- Indexes for table `prenotazioni`
--
ALTER TABLE `prenotazioni`
  ADD PRIMARY KEY (`id_prenotazione`),
  ADD KEY `FK_STUDENTI_PRENOTAZIONI` (`matricola`),
  ADD KEY `FK_PRENOTAZIONE_DATALEZIONE` (`id_data`);

--
-- Indexes for table `studente`
--
ALTER TABLE `studente`
  ADD PRIMARY KEY (`matricola`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `aula_fisica`
--
ALTER TABLE `aula_fisica`
  MODIFY `id_aula` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `corso`
--
ALTER TABLE `corso`
  MODIFY `id_corso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `data_lezione`
--
ALTER TABLE `data_lezione`
  MODIFY `id_data` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `docenti`
--
ALTER TABLE `docenti`
  MODIFY `id_docente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `lezioni`
--
ALTER TABLE `lezioni`
  MODIFY `id_lezione` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `prenotazioni`
--
ALTER TABLE `prenotazioni`
  MODIFY `id_prenotazione` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `data_lezione`
--
ALTER TABLE `data_lezione`
  ADD CONSTRAINT `FK_DATALEZIONE_LEZIONE` FOREIGN KEY (`id_lezione`) REFERENCES `lezioni` (`id_lezione`),
  ADD CONSTRAINT `FK_FATALEZIONI_AULAFISICA` FOREIGN KEY (`id_aula`) REFERENCES `aula_fisica` (`id_aula`);

--
-- Constraints for table `lezioni`
--
ALTER TABLE `lezioni`
  ADD CONSTRAINT `FK_LEZIONI_CORSO` FOREIGN KEY (`id_corso`) REFERENCES `corso` (`id_corso`),
  ADD CONSTRAINT `FK_LEZIONI_DOCENTE` FOREIGN KEY (`id_docente`) REFERENCES `docenti` (`id_docente`);

--
-- Constraints for table `prenotazioni`
--
ALTER TABLE `prenotazioni`
  ADD CONSTRAINT `FK_PRENOTAZIONE_DATALEZIONE` FOREIGN KEY (`id_data`) REFERENCES `data_lezione` (`id_data`),
  ADD CONSTRAINT `FK_STUDENTI_PRENOTAZIONI` FOREIGN KEY (`matricola`) REFERENCES `studente` (`matricola`);
COMMIT;