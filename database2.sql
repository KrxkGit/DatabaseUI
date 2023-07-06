/*
 Navicat Premium Data Transfer

 Source Server         : Johnson
 Source Server Type    : MySQL
 Source Server Version : 50738
 Source Host           : localhost:3306
 Source Schema         : database2

 Target Server Type    : MySQL
 Target Server Version : 50738
 File Encoding         : 65001

 Date: 06/07/2023 22:24:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for course_choosing
-- ----------------------------
DROP TABLE IF EXISTS `course_choosing`;
CREATE TABLE `course_choosing`  (
  `student_ID` int(11) NOT NULL,
  `teacher_ID` int(11) NOT NULL,
  `course_ID` int(11) NOT NULL,
  `chosen_year` int(11) NOT NULL,
  `score` int(11) NULL DEFAULT NULL,
  INDEX `student_ID`(`student_ID`) USING BTREE,
  INDEX `teacher_ID`(`teacher_ID`) USING BTREE,
  INDEX `course_ID`(`course_ID`) USING BTREE,
  CONSTRAINT `course_choosing_ibfk_1` FOREIGN KEY (`student_ID`) REFERENCES `students` (`student_ID`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `course_choosing_ibfk_2` FOREIGN KEY (`teacher_ID`) REFERENCES `teachers` (`teacher_ID`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `course_choosing_ibfk_3` FOREIGN KEY (`course_ID`) REFERENCES `courses` (`course_ID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course_choosing
-- ----------------------------
INSERT INTO `course_choosing` VALUES (10001, 1001, 101, 2023, 99);
INSERT INTO `course_choosing` VALUES (10001, 1001, 102, 2023, 86);
INSERT INTO `course_choosing` VALUES (10001, 1002, 103, 2023, 92);
INSERT INTO `course_choosing` VALUES (10001, 1003, 105, 2024, 92);
INSERT INTO `course_choosing` VALUES (10001, 1003, 106, 2024, 87);
INSERT INTO `course_choosing` VALUES (10002, 1001, 101, 2023, 88);
INSERT INTO `course_choosing` VALUES (10002, 1003, 105, 2024, 90);
INSERT INTO `course_choosing` VALUES (10002, 1002, 103, 2023, 82);

-- ----------------------------
-- Table structure for courses
-- ----------------------------
DROP TABLE IF EXISTS `courses`;
CREATE TABLE `courses`  (
  `course_ID` int(11) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `teacher_ID` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `credit` int(11) NOT NULL,
  `grade` int(11) NOT NULL,
  `canceled_year` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`course_ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of courses
-- ----------------------------
INSERT INTO `courses` VALUES (101, '高数', '1001', 4, 1, 2050);
INSERT INTO `courses` VALUES (102, '线性代数', '1001', 3, 1, 2050);
INSERT INTO `courses` VALUES (103, 'Python程序设计', '1002', 3, 1, 2050);
INSERT INTO `courses` VALUES (104, '算法设计', '1002', 3, 2, 2050);
INSERT INTO `courses` VALUES (105, 'C++程序设计', '1003', 4, 1, 2050);
INSERT INTO `courses` VALUES (106, '计算机组成与原理', '1003', 4, 2, 2050);
INSERT INTO `courses` VALUES (107, '计算机网络', '1003', 3, 2, 2050);
INSERT INTO `courses` VALUES (108, '计算机视觉', '1004', 3, 3, 2050);
INSERT INTO `courses` VALUES (109, '数字图像处理', '1004', 3, 3, 2050);
INSERT INTO `courses` VALUES (110, '中国近代史', '1005', 4, 1, 2050);
INSERT INTO `courses` VALUES (111, '毛泽东思想概论', '1005', 3, 1, 2050);
INSERT INTO `courses` VALUES (112, '思想道德与法治', '1005', 2, 2, 2050);
INSERT INTO `courses` VALUES (113, '电路与电子技术', '1006', 3, 2, 2050);
INSERT INTO `courses` VALUES (114, '电路与电子技术（实验）', '1006', 4, 2, 2050);
INSERT INTO `courses` VALUES (115, '算法竞赛', '1007', 4, 2, 2050);
INSERT INTO `courses` VALUES (116, '数据结构', '1007', 4, 1, 2050);

-- ----------------------------
-- Table structure for students
-- ----------------------------
DROP TABLE IF EXISTS `students`;
CREATE TABLE `students`  (
  `student_ID` int(11) NOT NULL,
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `sex` enum('male','female') CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `entrance_age` int(11) NOT NULL,
  `entrance_year` int(11) NOT NULL,
  `class` varchar(99) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`student_ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of students
-- ----------------------------
INSERT INTO `students` VALUES (10001, '李华', 'male', 22, 2021, '网络工程');
INSERT INTO `students` VALUES (10002, '王晓明', 'male', 20, 2023, '网络工程');
INSERT INTO `students` VALUES (10003, '武松', 'male', 20, 2023, '网络工程');
INSERT INTO `students` VALUES (10004, '老虎', 'female', 21, 2023, '网络工程');
INSERT INTO `students` VALUES (10005, '宋江', 'male', 20, 2023, '计科（全英创新班）');
INSERT INTO `students` VALUES (10006, '姚炯森', 'male', 20, 2023, '计科（全英创新班）');
INSERT INTO `students` VALUES (10007, '电脑', 'male', 20, 2023, '计科（全英创新班）');
INSERT INTO `students` VALUES (10011, '香蕉', 'male', 20, 2023, '计算机科学与技术');
INSERT INTO `students` VALUES (10012, '纸巾', 'female', 20, 2023, '计算机科学与技术');
INSERT INTO `students` VALUES (10013, '音乐', 'male', 20, 2023, '信息安全');
INSERT INTO `students` VALUES (10014, '歌曲', 'female', 20, 2023, '信息安全');
INSERT INTO `students` VALUES (10016, '刘备', 'male', 20, 2023, '信息安全');
INSERT INTO `students` VALUES (10017, '张飞', 'male', 21, 2023, '信息安全');
INSERT INTO `students` VALUES (10018, '王昭君', 'female', 21, 2023, '信息安全');

-- ----------------------------
-- Table structure for teachers
-- ----------------------------
DROP TABLE IF EXISTS `teachers`;
CREATE TABLE `teachers`  (
  `teacher_ID` int(11) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `course` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`teacher_ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teachers
-- ----------------------------
INSERT INTO `teachers` VALUES (1001, '周老师', '高数、线性代数');
INSERT INTO `teachers` VALUES (1002, '黄老师', 'Python程序设计、算法设计');
INSERT INTO `teachers` VALUES (1003, '李老师', 'C++程序设计、计算机组成与原理、计算机网络');
INSERT INTO `teachers` VALUES (1004, '陈老师', '计算机视觉、数字图像处理');
INSERT INTO `teachers` VALUES (1005, '高老师', '中国近代史、毛泽东思想概论、思想道德与法治');
INSERT INTO `teachers` VALUES (1006, '林老师', '电路与电子技术、电路与电子技术（实验）');
INSERT INTO `teachers` VALUES (1007, '姚老师', '算法竞赛、数据结构');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `account` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`account`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('admin', '123');
INSERT INTO `user` VALUES ('student', '123');
INSERT INTO `user` VALUES ('teacher', '123');

SET FOREIGN_KEY_CHECKS = 1;
