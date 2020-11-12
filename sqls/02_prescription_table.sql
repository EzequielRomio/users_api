CREATE TABLE prescriptions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    prescription_date TEXT NOT NULL,
    created_date TEXT NOT NULL, 
    od TEXT NOT NULL,
    oi TEXT NOT NULL,
    addition TEXT,
    notes TEXT,
    doctor TEXT   
);
