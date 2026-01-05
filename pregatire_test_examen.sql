--Pregatire lucrare/examen
--Curs Oracle

--Conversii de date
--Conversie de data -> caracter
describe angajati_dealer;
describe angajati;
select to_char(data_angajare, 'Month ddth - YYYY') from angajati_dealer;
select to_char(data_angajare, 'ddth Mon, YYYY') as Format_data_angajare from angajati;

--Conversie de la numar la caracter
describe salariati;
select to_char(salariul, '$9999.99') as Salariu from salariati;
select to_char(85000, '999,999.99') from dual;

--Conversie de la caracter la numar

select * from salariati;
select to_number('42,320', '99,999')as Numar from dual;
select nume ||''|| prenume as Nume_angajat, nvl2(telefon, 1, 0) as Numar_de_telefon from salariati;
select nume ||''|| prenume as Nume_angajat, nvl(telefon, 'unknown') as Numar_de_telefon from salariati;


--Conversie de la caracter la data

select to_date('October 28, 2005', 'Month, dd, YYYY') as Birthday from dual;
--to_date cu ajutorul corectorului fx:
select to_date('28October2005', 'fxddMonthYYYY') as Birthday from dual;


--Case/Decode

describe angajati;
select * from angajati;
select nume || ' ' || prenume as Nume_angajat,
case id_departament
    when 100 then 'FI_ACCOUNT'
    when 101 then 'PR_REP'
    when 50 then 'ST_CLERK'
    else 'OTHER DEPT.'
    end as Departament
from angajati;


select to_date('01-Jun-2004') - to_date('01-Oct-2004') from dual;

select next_day(hire_date) + 5 from dual;
select sysdate - 6 as DIferenta_de_data from dual;
select sysdate+30/24 from dual;

select prenume, 
decode(id_manager, 100, 'King', 'A N Other') "Works for?"
from angajati;

select 121/null from dual;

select avg(salariul), max(salariul), min(salariul), sum(salariul) from angajati;
select * from salariati;
select id_departament, id_manager, id_functie, sum(salariul)
from salariati
group by rollup(id_departament, id_manager);

select id_functie, count(*)
from angajati
group by id_functie;