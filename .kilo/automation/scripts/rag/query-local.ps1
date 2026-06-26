param(
  [Parameter(Mandatory=$true)]
  [string]$Query,

  [Parameter(Mandatory=$false)]
  [int]$Top = 5,

  [Parameter(Mandatory=$false)]
  [ValidateSet("commands","skills","agents","rules","memory","project-dna","decisions","knowledge","official","engineer-docs","root-docs","unknown")]
  [string]$SourceType = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($SourceType)) {
  py ./.kilo/automation/scripts/rag/rag_local.py query --query $Query --top $Top
} else {
  py ./.kilo/automation/scripts/rag/rag_local.py query --query $Query --top $Top --source-type $SourceType
}
