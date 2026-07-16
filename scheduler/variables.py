# variables.py
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

@dataclass
class Guru:
    id: str
    name: str
    max_hours_per_day: int = 6
    unavailability: List[Tuple[str, int]] = field(default_factory=list)  # [(hari, jam), ...]
    preferences: List[Tuple[str, int]] = field(default_factory=list)     # [(hari, jam), ...]

@dataclass
class Rombel:
    id: str
    name: str
    unavailability: List[Tuple[str, int]] = field(default_factory=list)  # [(hari, jam), ...]

@dataclass
class Mapel:
    id: str
    name: str
    duration: int = 2  # Durasi JP (Jam Pelajaran) sekaligus

@dataclass
class KelasAktif:
    """Representasi satu entitas kegiatan belajar mengajar yang harus dijadwalkan."""
    id: str
    rombel_id: str
    guru_id: str
    mapel_id: str
    room_requirements: List[str] = field(default_factory=list)

@dataclass
class Ruangan:
    id: str
    name: str
    is_lab: bool = False

@dataclass
class ScheduleAssignment:
    kelas_id: str
    rombel_id: str
    guru_id: str
    mapel_id: str
    hari: str
    jam_mulai: int
    durasi: int
    ruangan_id: str

@dataclass
class ScheduleResult:
    is_feasible: bool
    assignments: List[ScheduleAssignment] = field(default_factory=list)
    computation_time: float = 0.0
    unmapped_classes: List[str] = field(default_factory=list)
