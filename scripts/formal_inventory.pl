#!/usr/bin/env perl
use strict;
use warnings;

my $path = shift // die "usage: formal_inventory.pl FILE.lyx\n";
open my $fh, '<', $path or die "$path: $!\n";
my @lines = <$fh>;

my %formal = map { $_ => 1 } qw(Axiom Definition Fact Claim Lemma Proposition Corollary Theorem Proof Exercise Example);
$formal{'Exercise*'} = 1;
my ($chapter, $section) = ('', '');
print "line\ttype\tchapter\tsection\texcerpt\n";

for (my $i = 0; $i < @lines; $i++) {
    if ($lines[$i] =~ /^\\begin_layout (Chapter|Section)$/) {
        my $kind = $1;
        my $title = $lines[++$i] // '';
        chomp $title;
        if ($kind eq 'Chapter') { $chapter = $title; $section = ''; }
        else { $section = $title; }
        next;
    }
    next unless $lines[$i] =~ /^\\begin_layout ([\w*]+)$/ && $formal{$1};
    my ($kind, $start) = ($1, $i + 1);
    my @text;
    while (++$i < @lines && $lines[$i] !~ /^\\end_layout$/) {
        my $line = $lines[$i];
        chomp $line;
        if ($line =~ /^\\begin_inset Formula \$(.*)\$$/) {
            push @text, "\$$1\$";
        } elsif ($line =~ /^\\begin_inset Formula\s*$/) {
            my @formula;
            while (++$i < @lines && $lines[$i] !~ /^\\end_inset$/) {
                my $f = $lines[$i]; chomp $f;
                next if $f =~ /^\\?\[?\]?$/;
                push @formula, $f unless $f =~ /^\s*$/;
            }
            push @text, join(' ', @formula);
        } elsif ($line !~ /^\\/ && $line !~ /^\s*$/ && $line !~ /^(status|collapsed)/) {
            push @text, $line;
        }
    }
    my $excerpt = join(' ', @text);
    $excerpt =~ s/\s+/ /g;
    $excerpt =~ s/^\s+|\s+$//g;
    $excerpt = substr($excerpt, 0, 240);
    $excerpt =~ s/\s+$//;
    next if $kind =~ /^Exercise/ && $excerpt !~ /^Problem\s+[\w.]+\s+\[(?:Core|Proof|Applied)\]/;
    for ($chapter, $section, $excerpt) { s/\t/ /g; }
    print join("\t", $start, $kind, $chapter, $section, $excerpt), "\n";
}
