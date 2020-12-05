set foreign_key_checks = 0;

drop table if exists auth_group;                 
drop table if exists auth_group_permissions;     
drop table if exists auth_permission;            
drop table if exists auth_user;                  
drop table if exists auth_user_groups;           
drop table if exists auth_user_user_permissions; 
drop table if exists django_content_type;        
drop table if exists django_migrations;          
drop table if exists oj_judge;                   
drop table if exists oj_judge_problems;          
drop table if exists oj_judge_runtimes;          
drop table if exists oj_language;                
drop table if exists oj_problem;                 
drop table if exists oj_problem_curators;        
drop table if exists oj_profile;                 
drop table if exists oj_runtimeversion;          
drop table if exists oj_submission;              
drop table if exists oj_submissionsource;        
drop table if exists oj_submissiontestcase;

set foreign_key_checks = 1;