-- Look at crime_scene_reports and search for reports for the mentioned day
SELECT * FROM crime_scene_reports WHERE day = 28 AND month = 7 AND year = 2021 AND street = "Humphrey Street";

-- Find the interview transcripts of the three witnesses (mentioned bakery)
SELECT * FROM interviews WHERE transcript LIKE "%bakery%";

-- Check security logs within 10 minutes of the theft to get a licence plate
SELECT * FROM bakery_security_logs WHERE day = 28 AND month = 7 AND year = 2021 AND hour = 10;

-- Check ATM transactions on this day
SELECT * FROM atm_transactions WHERE day = 28 AND month = 7 AND year = 2021 AND atm_location ="Leggett Street" AND transaction_type = "withdraw";

-- Check which bank accounts goes with transactions to compare licence plates with people who made withdraws
SELECT * FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id JOIn atm_transactions On bank_accounts.account_number = atm_transactions.account_number WHERE atm_transactions.day = 28 AND atm_transactions.mont = 7 AND atm_transactions.year = 2021 AND atm_transactions.lo9cation = "Leggett Street" AND atm_transactions.transaction_tyoe = "withdraw";

-- Check first flight from Fiftyville on the next day and find destination
SELECT * FROM flights JOIN airports ON flights.origin_airport_id = airports.id WHERE day = 29 AND month = 7 AND year = 2021 AND city = "Fiftyville" ORDER BY hour;
SELECT * FROM airports WHERE id = 4;

-- Check passegners on earliest flights from Fiftyville on the next day
SELECT * FROM passengers JOIN flights ON passengers.flight_id = flights.id JOIN airports ON flights.origin_airport_id = airports.id WHERE airports.city = "Fiftyville" AND flights.day = 29 AND flights.month = 27 AND flights.year = 2021 ORDER BY flights.hour;

-- Check numbers of passengers and persons with the right bank accounts in phone calls on 28.07.2021
SELECT * FROM phone_calls WHERE day = 28 AND month = 7 AND year = 2021 AND caller = "(367) 555-5533";
SELECT * FROM phone_calls WHERE day = 28 AND month = 7 AND year = 2021 AND caller = "(389) 555-5198";

-- Check person who got called from Bruce with duration under 1 minute
SELECT * FROM people WHERE phone_numer = "(375) 555 8161";
