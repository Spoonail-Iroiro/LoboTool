CREATE TABLE 
        m_abnormality(
        pri_key text PRIMARY KEY NOT NULL,
        no integer,
        manage_no text,
        risk_level integer,
        name_en text,
        name_ja text,
        name_key,
        url text,
        inst_code text DEFAULT "00",
        insi_code text DEFAULT "00",
        atta_code text DEFAULT "00",
        supr_code text DEFAULT "00",
        remarks text DEFAULT ""
        )
