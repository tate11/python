#!/usr/local/bin/perl -s

use POSIX qw(ceil);

my $fs_bs = 4096;       # Set to your filesystem's block size.
my $my_bs = 32768;      # The size we will use (should be a multiple
                        # of $fs_bs).

my($f1,$f2) = @ARGV;
usage() if $#ARGV != 1;
usage("$f1 does not exist") if ! -f $f1;
usage("$f2 does not exist") if ! -f $f2;

my $f1_size = (stat($f1))[7];
my $f2_size = (stat($f2))[7];

# More indirect blocks may be required by combining the files.
my ($direct_pointers, $directs_relocate);
if ($^O =~ m/aix/i) {
    $direct_pointers  = 8;
    $directs_relocate = 1;   # Direct pointers move to 1st single 
                             # indirect.
} else {
    $direct_pointers  = 12;
    $directs_relocate = 0;   # Direct pointers remain in the inode.
}
my $indirect_pointers = $fs_bs / 4;     # Each pointer is 4 bytes.
my $f1_indirect       = num_indirect($f1_size);
my $f2_indirect       = num_indirect($f2_size);
my $combined_indirect = num_indirect($f1_size + $f2_size);
my $addtl_blocks      = $combined_indirect - ($f1_indirect + $f2_indirect);

# If the last block of each file is only partially used and the 
# amount in both is less than the size of a block, we'll save 
# a block by combining the files.
my $f1_pb = $f1_size % $fs_bs;
my $f2_pb = $f2_size % $fs_bs;
$addtl_blocks-- if $f1_pb > 0 && $f2_pb > 0 && $f1_pb + $f2_pb < $fs_bs;

die "It appears that $addtl_blocks additional block(s) will be \
     needed.\n" .
    "Make sure the space is available and re-run with -spaceok.\n"
    if ($addtl_blocks > 0 && ! $spaceok);

open(F2, "+<" . $f2) or die "open $f2: $!";
open(F1, "+<" . $f1) or die "open $f1: $!";

# Buffer enough to allow for new indirects before they are 
# relinquished from f1 (3, in case the first triple indirect 
# block is required).
$num_buf = ceil(3 * $fs_bs / $my_bs);

my @buffered;
while ($f1_size > 0) {
    push(@buffered, get_block());
    put_block(shift @buffered) if ($#buffered >= $num_buf);
}
put_block($_) while(defined($_ = shift @buffered));  # Flush buffered 
                                                     # blocks.

close F1;
close F2;
unlink($f1);

sub get_block {
    my ($this_bs, $buf);

    if (!defined @buffered) {                  # This is the 1st 
                                               # get_block call.
        $this_bs = $f1_size % $my_bs + $my_bs; # Align w/bs for 
                                               # performance.
    } else {
        $this_bs = $my_bs;
    }

    $f1_size -= $this_bs;
    $f1_size = 0 if $f1_size < 0;

    seek F1, $f1_size, 0    or die "$!";
    read F1, $buf, $this_bs or die "$!";
    truncate F1, $f1_size   or die "$!";

    return { data => $buf, offset => $f1_size };
}

sub put_block {
    my $buffered = $_[0];
    seek F2, $f2_size + $buffered->{offset}, 0 or die "seek $!";
    print F2 $buffered->{data} or die "print $!";
}

sub num_indirect {
    my $blks = ceil($_[0] / $fs_bs);
    my ($single, $double, $triple);

    return 0 if $blks <= $direct_pointers;    # No indirect blocks.
    $blks -= $direct_pointers unless $directs_relocate;

    $single = ceil($blks   / $indirect_pointers);
    $double = ceil($single / $indirect_pointers) if $single > 1;
    $triple = ceil($double / $indirect_pointers) if $double > 1;
    return $single + $double + $triple;
}

sub usage() {
    print "$_[0]\n" if $_[0];
    print "$0 [-spaceok] file1 file2\n";
    exit 1;
}

