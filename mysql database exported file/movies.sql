-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 23, 2021 at 06:21 PM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 8.0.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `movies`
--

-- --------------------------------------------------------

--
-- Table structure for table `genres`
--

CREATE TABLE `genres` (
  `username` varchar(255) NOT NULL,
  `genres` text NOT NULL,
  `day` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `genres`
--

INSERT INTO `genres` (`username`, `genres`, `day`) VALUES
('groot', 'Mystery', 'Tuesday'),
('groot', 'Mystery', 'Tuesday'),
('groot', 'Noir', 'Tuesday'),
('groot', 'Horror', 'Tuesday'),
('groot', 'Science Fiction', 'Tuesday'),
('groot', 'Science Fiction', 'Tuesday'),
('groot', 'Science Fiction', 'Tuesday'),
('groot', 'Drama', 'Tuesday'),
('groot', 'Crime', 'Tuesday'),
('groot', 'Thriller', 'Tuesday'),
('groot', 'Horror', 'Tuesday'),
('groot', 'Superhero', 'Tuesday'),
('groot', 'Superhero', 'Tuesday'),
('groot', 'Superhero', 'Tuesday'),
('groot', 'Family', 'Tuesday'),
('groot', 'Fantasy', 'Tuesday'),
('groot', 'Superhero', 'Tuesday'),
('groot', 'Science Fiction', 'Tuesday'),
('groot', 'Thriller', 'Tuesday'),
('groot', 'Action', 'Tuesday'),
('groot', 'Action', 'Tuesday'),
('groot', 'Adventure', 'Tuesday'),
('groot', 'Superhero', 'Tuesday'),
('groot', 'Comedy', 'Tuesday'),
('groot', 'Science Fiction', 'Tuesday'),
('groot', 'Crime', 'Tuesday'),
('groot', 'Thriller', 'Tuesday'),
('groot', 'Animated', 'Tuesday'),
('groot', 'Superhero', 'Tuesday'),
('groot', 'Action', 'Tuesday'),
('groot', 'Comedy', 'Tuesday');

-- --------------------------------------------------------

--
-- Table structure for table `searched`
--

CREATE TABLE `searched` (
  `username` varchar(255) NOT NULL,
  `keywords` text NOT NULL,
  `title` text NOT NULL,
  `day` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `searched`
--

INSERT INTO `searched` (`username`, `keywords`, `title`, `day`) VALUES
('groot', 'spider', 'The Spider', 'Tuesday'),
('groot', 'spider', 'The Spider Woman', 'Tuesday'),
('groot', 'spider', 'The Spider', 'Tuesday'),
('groot', 'spider', 'The Spider Woman Strikes Back', 'Tuesday'),
('groot', 'spider', 'Earth vs. the Spider', 'Tuesday'),
('groot', 'spider', 'The Giant Spider Invasion', 'Tuesday'),
('groot', 'spider', 'Kingdom of the Spiders', 'Tuesday'),
('groot', 'spider', 'Kiss of the Spider Woman', 'Tuesday'),
('groot', 'spider', 'Along Came a Spider', 'Tuesday'),
('groot', 'spider', 'Earth vs. the Spider', 'Tuesday'),
('groot', 'spider', 'Spider-Man', 'Tuesday'),
('groot', 'spider', 'Spider-Man 2', 'Tuesday'),
('groot', 'spider', 'Spider-Man 3', 'Tuesday'),
('groot', 'spider', 'The Spiderwick Chronicles', 'Tuesday'),
('groot', 'spider', 'The Amazing Spider-Man', 'Tuesday'),
('groot', 'spider', 'Big Ass Spider!', 'Tuesday'),
('groot', 'spider', 'Spiders 3D', 'Tuesday'),
('groot', 'spider', 'The Amazing Spider-Man 2', 'Tuesday'),
('groot', 'spider', 'Spider-Man: Homecoming', 'Tuesday'),
('groot', 'spider', 'The Girl in the Spider\'s Web', 'Tuesday'),
('groot', 'spider', 'Spider-Man: Into the Spider-Verse', 'Tuesday');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `email` text NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `firstname`, `lastname`, `email`, `username`, `password`) VALUES
(1, '', '', 'groot@test.com', 'groot', 'pbkdf2:sha256:260000$DCtjOFd6lDGfqed8$e74d35381d1fa955e01f6081686424cf4b94401dafe1a42cabc7fe3d7b01926f');

-- --------------------------------------------------------

--
-- Table structure for table `watched`
--

CREATE TABLE `watched` (
  `username` varchar(255) NOT NULL,
  `title` text NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `day` text NOT NULL,
  `time` text NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `watched`
--

INSERT INTO `watched` (`username`, `title`, `date`, `day`, `time`) VALUES
('groot', 'Humor Me', '2021-11-23 16:54:13', 'Tuesday', '21:54:13'),
('groot', 'Humor Me', '2021-11-23 16:54:38', 'Tuesday', '21:54:38'),
('groot', '12 Strong', '2021-11-23 16:54:55', 'Tuesday', '21:54:55'),
('groot', 'Den of Thieves', '2021-11-23 16:54:58', 'Tuesday', '21:54:58'),
('groot', 'Sweet Country', '2021-11-23 17:04:44', 'Tuesday', '22:04:44'),
('groot', 'After Dark in Central Park', '2021-11-23 17:09:34', 'Tuesday', '22:09:34');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
