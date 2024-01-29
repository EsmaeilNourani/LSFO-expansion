#!/usr/bin/perl -w

use strict;

my %name_priority = ();
open IN, "< ".$ARGV[0] or die;
while (<IN>) {
	s/\r?\n//;
	my ($serial, $name, $priority) = split /\t/;
	$name =~ s/[ -]+//g;
	$name_priority{lc $name} = $priority unless exists $name_priority{lc $name} and $name_priority{lc $name} <= $priority;
}
close IN;

open IN, "< ".$ARGV[0] or die;
while (<IN>) {
	s/\r?\n//;
	my ($serial, $name, $priority) = split /\t/;
	$name =~ s/[ -]+//g;
	print $_, "\n" unless $name_priority{lc $name} < $priority;
}
close IN;
