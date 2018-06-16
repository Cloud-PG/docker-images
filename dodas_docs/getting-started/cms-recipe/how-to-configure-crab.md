# How to configure CRAB

In order to submit CRAB jobs with proper classad parameters which guarantee the matching, you need to add this extra line in the configuration file of CRAB: 

`config.Debug.extraJDL = [ '+DESIRED_Sites="T3_XX_XY_KK"','+JOB_CMSSite="T3_XX_XY_KK"','+AccountingGroup="highprio.<YOUR_LXPLUS_LOGIN>"' ]`

There is no any other change you need to do. 

