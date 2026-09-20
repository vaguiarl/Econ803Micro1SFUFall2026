#!/usr/bin/env perl
use strict;
use warnings;

my $path = shift // die "usage: book_map.pl FILE.lyx\n";
open my $fh, '<', $path or die "$path: $!\n";
my @lines = <$fh>;

sub layout_text {
    my ($start) = @_;
    my @text;
    for (my $j = $start + 1; $j < @lines && $lines[$j] !~ /^\\end_layout$/; $j++) {
        my $line = $lines[$j];
        chomp $line;
        if ($line =~ /^\\begin_inset Formula \$(.*)\$$/) {
            push @text, "\$$1\$";
        } elsif ($line !~ /^\\/ && $line !~ /^\s*$/ && $line !~ /^(status|collapsed)/) {
            push @text, $line;
        }
    }
    my $text = join(' ', @text);
    $text =~ s/\s+/ /g;
    $text =~ s/^\s+|\s+$//g;
    return $text;
}

my %formal = map { $_ => 1 } qw(Axiom Definition Fact Claim Lemma Proposition Corollary Theorem Proof Exercise Example);
$formal{'Exercise*'} = 1;
my (@chapters, %seen_chapter, %part_for, %sections, %formal_count, %section_count);
my ($part, $chapter) = ('Front matter', '');

for (my $i = 0; $i < @lines; $i++) {
    if ($lines[$i] =~ /^appendix\s*$/) {
        $part = 'Mathematical appendices';
        next;
    }
    if ($lines[$i] =~ /^\\begin_layout (Part|Chapter|Section|Subsection)$/) {
        my ($kind, $title) = ($1, layout_text($i));
        if ($kind eq 'Part') {
            $part = $title;
        } elsif ($kind eq 'Chapter') {
            $chapter = $title;
            if (!$seen_chapter{$chapter}++) {
                push @chapters, $chapter;
                $part_for{$chapter} = $part;
            }
        } elsif ($chapter ne '') {
            push @{$sections{$chapter}}, [$kind, $title];
            $section_count{$title}++ if $kind eq 'Section';
        }
        next;
    }
    if ($lines[$i] =~ /^\\begin_layout Chapter\*$/) {
        my $title = layout_text($i);
        if ($title eq 'Additional Practice Reserve') {
            $chapter = $title;
            if (!$seen_chapter{$chapter}++) {
                push @chapters, $chapter;
                $part_for{$chapter} = 'Supplemental material';
            }
        } elsif ($title eq 'Weekly Problem Sets: Fall 2026') {
            # This is a schedule, not a book chapter.  Clear the current
            # chapter so its unnumbered weekly headings are not attributed to
            # the assessment reserve.
            $chapter = '';
        }
        next;
    }
    if ($chapter eq 'Additional Practice Reserve' &&
        $lines[$i] =~ /^\\begin_layout Section\*$/) {
        my $title = layout_text($i);
        push @{$sections{$chapter}}, ['Section', $title];
        $section_count{$title}++;
        next;
    }
    if ($chapter ne '' && $lines[$i] =~ /^\\begin_layout ([\w*]+)$/ && $formal{$1}) {
        my $kind = $1;
        # Consecutive LyX Exercise layouts are exported as one theorem
        # environment.  Generated problem starts have a stable editorial
        # label; continuation paragraphs do not and must not be double-counted.
        next if $kind =~ /^Exercise/ && layout_text($i) !~ /^Problem\s+[\w.]+\s+\[(?:Core|Proof|Applied)\]/;
        $formal_count{$chapter}{$kind}++;
    }
}

print "# Book map and duplication index\n\n";
print "Generated from the LyX source by `scripts/book_map.pl`. Generated problems are counted once at their labelled opening paragraph. Other formal counts are LyX layout counts.\n\n";
print "| Part | Chapter | Definitions | Results | Proofs | Exercises/examples |\n";
print "|---|---|---:|---:|---:|---:|\n";
for my $ch (@chapters) {
    my $c = $formal_count{$ch} // {};
    my $results = ($c->{Theorem} // 0) + ($c->{Proposition} // 0) + ($c->{Lemma} // 0) + ($c->{Corollary} // 0) + ($c->{Claim} // 0) + ($c->{Fact} // 0);
    my $examples = ($c->{Exercise} // 0) + ($c->{'Exercise*'} // 0) + ($c->{Example} // 0);
    print "| $part_for{$ch} | $ch | ", ($c->{Definition} // 0), " | $results | ", ($c->{Proof} // 0), " | $examples |\n";
}

print "\n## Detailed sequence\n\n";
for my $ch (@chapters) {
    print "### $ch\n\n";
    for my $entry (@{$sections{$ch} // []}) {
        my ($kind, $title) = @$entry;
        my $indent = $kind eq 'Subsection' ? '  -' : '-';
        print "$indent $title\n";
    }
    print "\n";
}

print "## Repeated section titles\n\n";
my @duplicates = sort { $section_count{$b} <=> $section_count{$a} || $a cmp $b }
                 grep { $section_count{$_} > 1 } keys %section_count;
if (@duplicates) {
    print "| Section title | Occurrences |\n|---|---:|\n";
    print "| $_ | $section_count{$_} |\n" for @duplicates;
} else {
    print "No exact duplicate section titles.\n";
}
