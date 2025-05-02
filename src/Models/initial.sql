DROP TABLE IF EXISTS master_resumes;
DROP TABLE IF EXISTS slave_resumes;
DROP TABLE IF EXISTS job_postings;
DROP TABLE IF EXISTS job_details;
DROP TABLE IF EXISTS matches;

CREATE TABLE master_resumes (
    -- using uuid cause I don't know the scale of unique ids that I may need
    resume_id uuid default gen_random_uuid(),
    first_name varchar(100),
    middle_name varchar(100),
    last_name varchar(100),
    links json,
    email varchar(100),
    phone varchar(20),
    location varchar(100),
    summary varchar(1000),
    skills json,
    work_experience json,
    education json,
    projects json,
    date_added date,
    last_updated timestamptz,
    PRIMARY KEY(resume_id)
);

CREATE TABLE slave_resumes (
    slave_id int GENERATED ALWAYS AS IDENTITY,
    resume_id uuid,
    first_name varchar(100),
    middle_name varchar(100),
    last_name varchar(100),
    links json,
    email varchar(100),
    phone varchar(20),
    location varchar(100),
    summary varchar(1000),
    skills json,
    work_experience json,
    education json,
    projects json,
    date_added date,
    last_updated timestamptz,
    PRIMARY KEY(slave_id),
    CONSTRAINT fk_resume
        FOREIGN KEY(resume_id)
            REFERENCES master_resumes(resume_id)
);

CREATE TABLE job_postings (
    job_id uuid default gen_random_uuid(),
    job_type varchar(50),
    website text,
    url text,
    location varchar(100),
    company varchar(100),
    position varchar(100),
    work_shift varchar(50),
    work_setting varchar(50),
    date_added date,
    last_updated timestamptz,
    PRIMARY KEY(job_id)
);

CREATE TABLE job_details (
    job_id uuid,
    skills json,
    licences json,
    certifications json,
    education json,
    benefits json,
    full_job_description text,
    CONSTRAINT fk_job
        FOREIGN KEY(job_id)
        REFERENCES job_postings(job_id)
);

CREATE TABLE matches (
    match_id int GENERATED ALWAYS AS IDENTITY,
    job_id uuid,
    resume_id uuid,
    slave_id int,
    date_added date,
    last_updated timestamptz,
    CONSTRAINT fk_job
        FOREIGN KEY(job_id)
        REFERENCES job_postings(job_id),
    CONSTRAINT fk_resume
        FOREIGN KEY(resume_id)
            REFERENCES master_resumes(resume_id),
    CONSTRAINT fk_slave
        FOREIGN KEY(slave_id)
        REFERENCES slave_resumes(slave_id)
);
