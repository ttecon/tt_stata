version 13
set more off
adopath + ../ado
preliminaries

program main
    setup_data
    local csvlist = r(csvlist)
    tempfile tempmerged

    * Test dta files
    testgood load_and_append ./temp/file1 ./temp/file2 ./temp/file3, clear
    testgood load_and_append ./temp/file1.dta ./temp/file2.dta ./temp/file3.dta, clear
    sort x y
    qui save "`tempmerged'", replace

    * Test tsv files
    testgood load_and_append ./temp/delim/file1.txt ./temp/delim/file2.txt ./temp/delim/file3.txt, clear import
    sort x y
    testgood cf * using "`tempmerged'"

    * Test csv files
    testgood load_and_append ./temp/delim/file1.csv ./temp/delim/file2.csv ./temp/delim/file3.csv, clear import
    sort x y
    testgood cf * using `"`tempmerged'"'

    * Test dir() option
    testgood load_and_append file1 file2 file3, dir(./temp) clear
    testgood load_and_append file1 file2 file3, dir(./temp/) clear
    testgood load_and_append file1.txt file2.txt file3.txt, dir(./temp/delim/) import clear
    testgood load_and_append delim/file1.txt delim/file2.txt delim/file3.txt, dir(./temp/) import clear
    sort x y
    testgood cf * using `"`tempmerged'"'

    * Test wildcards
    testgood load_and_append file*, dir(./temp) clear
    testgood load_and_append file*.dta, dir(./temp) clear
    testgood load_and_append ./temp/file*.dta, clear
    testgood load_and_append ./temp/delim/file*.txt, clear import
    sort x y
    testgood cf * using `"`tempmerged'"'

    * Test clear
    testbad load_and_append ./temp/file1 ./temp/file2 ./temp/file3
    clear
    testgood load_and_append ./temp/file1 ./temp/file2 ./temp/file3
    sort x y
    testgood cf * using `"`tempmerged'"'

    * Test import_options
    testbad load_and_append ./temp/delim/file1.csv ./temp/delim/file2.csv ./temp/delim/file3.csv, ///
        clear import import_options(blah)
    testgood load_and_append ./temp/delim/file1.csv ./temp/delim/file2.csv ./temp/delim/file3.csv, ///
        clear import import_options(case(preserve))
    sort x y
    testgood cf * using `"`tempmerged'"'

    * Test append_options
    testbad load_and_append ./temp/file1 ./temp/file2 ./temp/file3, clear append_options(blah)
    testgood load_and_append ./temp/file1 ./temp/file2 ./temp/file3, clear append_options(force)
    sort x y
    testgood cf * using `"`tempmerged'"'

    * Test breaks if list has only one file
    testbad load_and_append ./temp/file1, clear

    * Test backslashes
    testgood load_and_append .\temp\file1 .\temp\file2 .\temp\file3, clear
    testgood load_and_append file1 file2 file3, dir(.\temp) clear
    testgood load_and_append file1 file2 file3, dir(.\temp\) clear

    * Test dsid
    testgood load_and_append ./temp/file1 ./temp/file2 ./temp/file3, clear dsid(studynumber)

    * Test dsname
    testgood load_and_append ./temp/file1 ./temp/file2 ./temp/file3, clear dsname(study_name)

    * Test obsseq
    testgood load_and_append ./temp/file1 ./temp/file2 ./temp/file3, clear obsseq(obs_order)

    * Test subset
    testgood load_and_append ./temp/file1 ./temp/file2 ./temp/file3, clear subset(x)
    testbad load_and_append ./temp/file1 ./temp/file2 ./temp/file3, clear subset(z)

    * Test fast
    testgood load_and_append ./temp/file1 ./temp/file2 ./temp/file3, clear fast
    use ./temp/file1, clear
    local orig = c(filename)
    testbad load_and_append ./temp/file2 ./temp/file3 ./temp/file5, clear fast
    local test = c(filename)
    assert "`orig'" != "`test'"

    cleanup
end

program setup_data
    cap mkdir temp
    cap mkdir temp/delim
    foreach i of numlist 1/3 {
        quietly {
            clear
            set obs 100
            foreach var in x y {
                gen `var' = round(uniform(), 0.001)
            }

            save ./temp/file`i'.dta, replace
            export delimited using ./temp/delim/file`i'.txt, replace

            tempfile csvfile`i'
            export delimited using ./temp/delim/file`i'.csv, replace
        }
    }
end

program cleanup
    foreach i of numlist 1/3 {
        rm temp/file`i'.dta
        rm temp/delim/file`i'.csv
        rm temp/delim/file`i'.txt
    }
   capture  rmdir temp/delim
   capture  rmdir temp
end

* EXECUTE
main









