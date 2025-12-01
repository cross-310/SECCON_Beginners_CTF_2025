add-type '
using System;
using System.Runtime.InteropServices;

[StructLayout( LayoutKind.Sequential )]
public static class Kernel32{
	[DllImport( "kernel32.dll" )]
	public static extern IntPtr VirtualAlloc( IntPtr address, int size, int AllocType, int protect );
}

public static class Rpcrt4{
	[DllImport( "rpcrt4.dll" )]
	public static extern void UuidFromStringA( string uuid, IntPtr buf );
}';

$workdir = ( Get-Location ).Path;
[System.IO.Directory]::SetCurrentDirectory( $workdir );
$lines = [System.IO.File]::ReadAllLines( ".\sh.txt" );
$size = $lines.Length * 16
$buf = [Kernel32]::VirtualAlloc( [IntPtr]::Zero, $lines.Length * 16, 0x1000, 0x40 );
$proc = $buf;
foreach( $line in $lines ){
	$tmp = [Rpcrt4]::UuidFromStringA( $line, $buf );
	$buf = [IntPtr]( $buf.ToInt64() + 16 )
}

$bytes = New-Object System.Byte[] $size
[System.Runtime.InteropServices.Marshal]::Copy( $proc, $bytes, 0, $size )
[System.IO.File]::WriteAllBytes( "shellcode.dat", $bytes )
