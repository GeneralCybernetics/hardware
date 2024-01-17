#!/usr/bin/perl -w -i.bak

while (<>) {
    chomp;
    if (/^\s*\(fp_text reference ([^\s]+)/) {
        my $ref = $1;
        unless (/ hide$/) {
            unless ($ref =~ /^J/ or $ref =~ /^TP/) {
                $_ .= " hide";
            }
        }
    }
    print $_, "\n";
}
