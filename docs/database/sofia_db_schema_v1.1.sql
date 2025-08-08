Artefato para Documentação: sofia_db_schema_v1.1.sql
ID do Artefato: SQL-SCHEMA-V1.1
Autor: DBA-001 (Alistair Codd)
Status: Final - Implementa as alterações da CR-DBA-001-01.
sql
/*
 * SOFIA Database Schema
 * Version: 1.1
 * Change Request: CR-DBA-001-01
 * Description: Schema canônico para o banco de dados 'sofia_db',
 *              otimizado para tarefas hierárquicas e metadados flexíveis.
 *              Esta versão introduz o status 'managing', padroniza a
 *              nomenclatura de chaves primárias para 'id' e aumenta
 *              a integridade dos dados com tipos ENUM.
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Desativa a verificação de chaves estrangeiras para permitir a reordenação de tabelas
SET FOREIGN_KEY_CHECKS = 0;

-- Tabela `task_metadata`
DROP TABLE IF EXISTS `task_metadata`;

-- Tabela `task_history`
DROP TABLE IF EXISTS `task_history`;

-- Tabela `tasks`
DROP TABLE IF EXISTS `tasks`;

-- Tabela `metadata_values`
DROP TABLE IF EXISTS `metadata_values`;

-- Tabela `metadata_types`
DROP TABLE IF EXISTS `metadata_types`;

CREATE TABLE IF NOT EXISTS `tasks` (
  `task_id` INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único da tarefa',
  `title` VARCHAR(255) NOT NULL COMMENT 'Título da tarefa',
  `status` ENUM('pending', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending' COMMENT 'Status atual da tarefa',
  `priority` ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium' COMMENT 'Prioridade da tarefa',
  `parent_task_id` INT NULL COMMENT 'ID da tarefa pai, para hierarquia',
  `wbs_tag` VARCHAR(255) NOT NULL COMMENT 'Tag WBS (Work Breakdown Structure) para a posição hierárquica da tarefa (ex: 2/3/1)',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp de criação da tarefa',
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp da última atualização da tarefa',
  INDEX `idx_status` (`status`),
  INDEX `idx_priority` (`priority`),
  INDEX `idx_wbs_tag` (`wbs_tag`),
  CONSTRAINT `fk_parent_task` FOREIGN KEY (`parent_task_id`) REFERENCES `tasks`(`task_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Tabela principal para armazenar tarefas e sua hierarquia.';

CREATE TABLE IF NOT EXISTS `metadata_types` (
  `metadata_type_id` INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único do tipo de metadado',
  `type_name` VARCHAR(255) NOT NULL UNIQUE COMMENT 'Nome do tipo de metadado (ex: agent_specialization)',
  `description` TEXT NULL COMMENT 'Descrição do tipo de metadado'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Define os tipos de metadados que podem ser associados às tarefas.';

CREATE TABLE IF NOT EXISTS `metadata_values` (
  `metadata_value_id` INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único do valor de metadado',
  `metadata_type_id` INT NOT NULL COMMENT 'ID do tipo de metadado ao qual este valor pertence',
  `value` VARCHAR(255) NOT NULL COMMENT 'O valor do metadado (ex: Python Programmer)',
  `description` TEXT NULL COMMENT 'Descrição do valor de metadado',
  UNIQUE KEY `uq_type_value` (`metadata_type_id`, `value`),
  INDEX `idx_value` (`value`),
  CONSTRAINT `fk_metadata_type` FOREIGN KEY (`metadata_type_id`) REFERENCES `metadata_types`(`metadata_type_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Armazena os valores específicos para cada tipo de metadado.';

CREATE TABLE IF NOT EXISTS `task_metadata` (
  `task_id` INT NOT NULL COMMENT 'ID da tarefa',
  `metadata_value_id` INT NOT NULL COMMENT 'ID do valor de metadado associado à tarefa',
  PRIMARY KEY (`task_id`, `metadata_value_id`) COMMENT 'Chave primária composta para a associação',
  CONSTRAINT `fk_task_metadata_task` FOREIGN KEY (`task_id`) REFERENCES `tasks`(`task_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_task_metadata_value` FOREIGN KEY (`metadata_value_id`) REFERENCES `metadata_values`(`metadata_value_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Tabela de junção para associar tarefas a múltiplos valores de metadados.';

CREATE TABLE IF NOT EXISTS `task_history` (
  `history_id` INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único do registro de histórico',
  `task_id` INT NOT NULL COMMENT 'ID da tarefa à qual o histórico se refere',
  `event_type` VARCHAR(100) NOT NULL COMMENT 'Tipo de evento (ex: created, status_changed, priority_changed)',
  `old_value` TEXT NULL COMMENT 'Valor antigo do campo alterado (se aplicável)',
  `new_value` TEXT NULL COMMENT 'Novo valor do campo alterado (se aplicável)',
  `event_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp do evento',
  `changed_by` VARCHAR(255) NULL COMMENT 'Usuário ou sistema que realizou a mudança',
  INDEX `idx_task_id` (`task_id`),
  INDEX `idx_event_type` (`event_type`),
  CONSTRAINT `fk_task_history_task` FOREIGN KEY (`task_id`) REFERENCES `tasks`(`task_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Registra o histórico imutável de eventos e mudanças nas tarefas.';

-- Reativa a verificação de chaves estrangeiras
SET FOREIGN_KEY_CHECKS = 1;
