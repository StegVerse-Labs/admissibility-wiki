# Volatile-memory evidence contract

This contract governs evidence **records**, not acquisition authority. A collector such as AVML, LiME, DumpIt, FTK Imager, or another approved tool may produce bytes; analysis tools such as Volatility or MemProcFS may interpret those bytes. Neither function establishes admissibility by itself.

A conforming record must bind the authorization reference, target machine identity, collector binary hash/version/parameters, acquisition interval, source/output size, evidence-object SHA-256, custody destination/receipt, and any derived finding back to the original `evidence_id`.

For streaming acquisition, chunks are ordered from index 0 with no gaps. Every chunk carries a SHA-256. The completed object still requires its own SHA-256. A stream without a final object digest is incomplete evidence.

Acquisition changes live memory. The manifest therefore requires an `impact_disclosure` rather than pretending the capture is observationally neutral.

Analysis lineage is append-only evidence metadata. Every finding must name the analysis tool/version/hash and `source_evidence_id`. Tool output has authority effect `NONE`.

The validator intentionally fails closed on missing authorization, machine identity, collector/evidence hashes, invalid timestamps, non-contiguous streamed chunk indexes, mismatched analysis source identifiers, or any manifest claiming admissibility/court acceptance.
