#!/bin/tclsh

load tclrega.so

set program_id "-1"
set active ""
set visible ""

catch {
	set input $env(QUERY_STRING)
	set pairs [split $input &]
	foreach pair $pairs {
		if {0 != [regexp "^(\[^=]*)=(.*)$" $pair dummy varname val]} {
			set $varname $val
		}
	}
}


puts -nonewline {Content-Type: text/xml
Access-Control-Allow-Origin: *

<?xml version="1.0" encoding="ISO-8859-1" ?><result>}

array set res [rega_script "
		if ($program_id > 0) { object obj = dom.GetObject($program_id); 
			if (obj && obj.IsTypeOf(OT_PROGRAM)) { 
				if ($active == false | $active == true){
					obj.Active($active);
				}
				if ($visible == false | $visible == true){
					obj.Visible($visible); 
				}
				Write(obj); 
			}
		}"]

if { $res(STDOUT) != "" } {
	puts -nonewline "<actions program_id=\"$program_id\" active=\"$active\" visible=\"$visible\"/>"
} else {
	puts -nonewline {<not_found/>}
}

puts -nonewline {</result>}
