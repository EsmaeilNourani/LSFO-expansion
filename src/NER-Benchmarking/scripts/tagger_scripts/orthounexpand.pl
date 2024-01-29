#!/usr/bin/perl -w

use strict;
use POSIX;

my %serial_ignore = ();
open IN, "< ".$ARGV[0] or die;
while (<IN>) {
	s/\r?\n//;
	my ($serial, $type, undef) = split /\t/;
	$serial_ignore{$serial} = 1 unless $type == -11;
}

my %original = ();
open IN, "< ".$ARGV[1] or die;
while (<IN>) {
	s/\r?\n//;
	my ($serial, $name, undef) = split /\t/;
	next if exists $serial_ignore{$serial};
	$name =~ s/[ -]+//g;
	$original{$serial."\t".lc($name)} = 1;
}
close IN;

my %expanded = ();
open IN, "< ".$ARGV[2] or die;
while (<IN>) {
        s/\r?\n//;
        my ($serial, $name) = split /\t/;
	next if exists $serial_ignore{$serial};
        $name =~ s/[ -]+//g;
	$expanded{lc($name)} = 0 unless exists $original{$serial."\t".lc($name)};
}
close IN;

open IN, "< ".$ARGV[1];
while (<IN>) {
        s/\r?\n//;
        my ($serial, $name, undef) = split /\t/;
	next if exists $serial_ignore{$serial};
        $name =~ s/[ -]+//g;
        $expanded{lc($name)} = 1 if exists $expanded{lc($name)};
}
close IN;

open IN, "< ".$ARGV[2];
while (<IN>) {
        s/\r?\n//;
        my ($serial, $name) = split /\t/;
        $name =~ s/[ -]+//g;
	print $_, "\n" unless exists $expanded{lc($name)} and $expanded{lc($name)} == 1 and not exists $original{$serial."\t".lc($name)} and not exists $serial_ignore{$serial};;
}
close IN;

close STDERR;
close STDOUT;
POSIX::_exit(0);
