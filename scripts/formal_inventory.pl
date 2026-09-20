#!/usr/bin/env perl
use strict;
use warnings;

my $path = shift // die "usage: formal_inventory.pl FILE.lyx\n";
open my $fh, '<', $path or die "$path: $!\n";
my @lines = <$fh>;

# LyX represents each paragraph as a layout. Consecutive paragraphs with the
# same theorem layout export as one LaTeX environment, so they must be grouped
# before counting. Some older proofs in this manuscript are delimited by raw
# \begin{proof}/\end{proof} ERT in otherwise Standard layouts; those blocks are
# recognized separately below.
my %formal = map { $_ => 1 } qw(
  Axiom Definition Fact Claim Lemma Proposition Corollary Theorem Proof
  Exercise Example ReaderTheorem FullTheorem
);
$formal{'Exercise*'} = 1;
$formal{'Theorem*'} = 1;

sub top_level_layouts {
    my ($source) = @_;
    my @blocks;
    my ($depth, $current) = (0, undef);

    for (my $i = 0; $i < @$source; $i++) {
        my $line = $source->[$i];
        if ($line =~ /^\\begin_layout (.+)$/) {
            if ($depth == 0) {
                my $kind = $1;
                chomp $kind;
                $current = {
                    kind  => $kind,
                    start => $i + 1,
                    raw   => [],
                };
            }
            $depth++;
        }

        push @{$current->{raw}}, $line if $depth > 0 && defined $current;

        if ($line =~ /^\\end_layout\s*$/ && $depth > 0) {
            $depth--;
            if ($depth == 0) {
                $current->{end} = $i + 1;
                push @blocks, $current;
                $current = undef;
            }
        }
    }

    die "$path: unterminated top-level LyX layout\n" if $depth != 0;
    return @blocks;
}

sub block_raw_text {
    my ($block) = @_;
    return join('', @{$block->{raw}});
}

sub contains_ert_proof_start {
    my ($block) = @_;
    return block_raw_text($block) =~ /(?:^|\n)begin\{proof\}(?:\s|$)/;
}

sub contains_ert_proof_end {
    my ($block) = @_;
    return block_raw_text($block) =~ /(?:^|\n)end\{proof\}(?:\s|$)/;
}

sub excerpt_from_blocks {
    my (@blocks) = @_;
    my $raw = join('', map { @{$_->{raw}} } @blocks);

    # Inline math in LyX may begin after prose and end on the next physical
    # line. Collapse those insets before the line-oriented pass so neither the
    # inset marker nor end marker leaks into the human-readable excerpt.
    $raw =~ s{\\begin_inset Formula \$([^\r\n]*)\$\r?\n\\end_inset}{\$$1\$}g;
    my @source = split(/(?<=\n)/, $raw);
    my @text;

    for (my $i = 0; $i < @source; $i++) {
        my $line = $source[$i];
        chomp $line;

        # LyX sometimes keeps a short formula inset on a single line of prose.
        $line =~ s/\\begin_inset Formula \$(.*?)\$\\end_inset/\$$1\$/g;

        if ($line =~ /^\s*\\begin_inset Formula \$(.*)\$\s*$/) {
            push @text, "\$$1\$";
            next;
        }

        if ($line =~ /^\s*\\begin_inset Formula\s*$/) {
            my @formula;
            while (++$i < @source && $source[$i] !~ /^\s*\\end_inset\s*$/) {
                my $formula_line = $source[$i];
                chomp $formula_line;
                $formula_line =~ s/^\s+|\s+$//g;
                next if $formula_line =~ /^(?:\\\[|\\\])$/;
                push @formula, $formula_line unless $formula_line =~ /^\s*$/;
            }
            push @text, join(' ', @formula);
            next;
        }

        # Render citations compactly instead of leaking LyX inset metadata.
        if ($line =~ /^\s*\\begin_inset CommandInset citation\s*$/) {
            my ($command, $keys) = ('cite', '');
            while (++$i < @source && $source[$i] !~ /^\s*\\end_inset\s*$/) {
                my $citation_line = $source[$i];
                chomp $citation_line;
                $command = $1 if $citation_line =~ /^LatexCommand\s+(\S+)/;
                $keys = $1 if $citation_line =~ /^key\s+"(.*)"/;
            }
            push @text, "\\$command\{$keys\}" if length $keys;
            next;
        }

        # ERT contains control code, including the proof delimiters. It is not
        # prose and should never appear in an excerpt.
        if ($line =~ /^\s*\\begin_inset ERT\s*$/) {
            while (++$i < @source && $source[$i] !~ /^\s*\\end_inset\s*$/) { }
            next;
        }

        next if $line =~ /^\s*\\/;
        next if $line =~ /^\s*$/;
        next if $line =~ /^(?:status|collapsed)\b/;
        next if $line =~ /^(?:begin|end)\{proof\}$/;
        push @text, $line;
    }

    my $excerpt = join(' ', @text);
    $excerpt =~ s/\s+/ /g;
    $excerpt =~ s/^\s+|\s+$//g;
    $excerpt = substr($excerpt, 0, 240);
    $excerpt =~ s/\s+$//;
    return $excerpt;
}

sub print_record {
    my ($start, $kind, $chapter, $section, $excerpt) = @_;
    return if $kind =~ /^Exercise/ &&
      $excerpt !~ /^Problem\s+[\w.]+\s+\[(?:Core|Proof|Applied)\]/;
    for ($chapter, $section, $excerpt) { s/\t/ /g; }
    print join("\t", $start, $kind, $chapter, $section, $excerpt), "\n";
}

my @blocks = top_level_layouts(\@lines);
my ($chapter, $section) = ('', '');
print "line\ttype\tchapter\tsection\texcerpt\n";

for (my $i = 0; $i < @blocks; $i++) {
    my $block = $blocks[$i];
    my $kind = $block->{kind};

    if ($kind eq 'Chapter' || $kind eq 'Section') {
        my $title = excerpt_from_blocks($block);
        if ($kind eq 'Chapter') {
            $chapter = $title;
            $section = '';
        } else {
            $section = $title;
        }
        next;
    }

    if ($kind eq 'Chapter*') {
        my $title = excerpt_from_blocks($block);
        if ($title eq 'Additional Practice Reserve') {
            $chapter = $title;
            $section = '';
        } elsif ($title eq 'Weekly Problem Sets: Fall 2026') {
            # Do not leave later formal records attached to the reserve.
            $chapter = '';
            $section = '';
        }
        next;
    }

    if ($kind eq 'Section*' && $chapter eq 'Additional Practice Reserve') {
        $section = excerpt_from_blocks($block);
        next;
    }

    if (contains_ert_proof_start($block)) {
        my @proof_blocks = ($block);
        while (!contains_ert_proof_end($proof_blocks[-1])) {
            $i++;
            die "$path:$block->{start}: ERT proof has no matching end{proof}\n"
              if $i >= @blocks;
            push @proof_blocks, $blocks[$i];
        }
        my $excerpt = excerpt_from_blocks(@proof_blocks);
        print_record($block->{start}, 'Proof', $chapter, $section, $excerpt);
        next;
    }

    next unless $formal{$kind};

    # Consecutive paragraphs with the same formal layout are a single exported
    # theorem/example/exercise environment.
    my @group = ($block);
    while ($i + 1 < @blocks && $blocks[$i + 1]->{kind} eq $kind) {
        $i++;
        push @group, $blocks[$i];
    }

    my $excerpt = excerpt_from_blocks(@group);
    print_record($block->{start}, $kind, $chapter, $section, $excerpt);
}
