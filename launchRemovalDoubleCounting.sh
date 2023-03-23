for cut in 000 001 002
do
        if [ -e analyzed/Data_$cut$nelec.root ]; then
                ./removeDoubleCounting.py analyzed/Data_$cut$nelec.root
                ./processCounting.py analyzed/Data_$cut$nelec.root analyzed/newData.root jobconfiganalysis
                mv analyzed/newData_$cut$nelec.root analyzed/Data_$cut$nelec.root
                rm analyzed/newData*
        fi
done

