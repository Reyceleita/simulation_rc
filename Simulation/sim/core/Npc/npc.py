"""
npc.py
Main NPC class. Thin orchestrator — delegates to specialised modules.

Dependency graph:
    NPC
    ├── NPCStats    (npc_stats.py)   — raw numerical state
    ├── NPCMemory   (npc_memory.py)  — short-term + emotional memory
    ├── NPCSocial   (npc_social.py)  — relationships & interactions
    ├── npc_drives  (npc_drives.py)  — drive calculation + action selection
    └── npc_actions (npc_actions.py) — action execution
"""

from sim.core.Npc_AI.planner.planner import Planner
from sim.core.Npc.npc_stats import NPCStats
from sim.core.Npc.npc_memory import NPCMemory
from sim.core.Npc.npc_social import NPCSocial
from sim.snapshots.decision_snapshot import DecisionSnapshot
from sim.core.Npc_AI.npc_drives import select_action
from sim.core.Npc_AI.npc_actions import execute_action
from sim.core.Npc_AI.executer import update as execute_plan

from collections import deque

class NPC:
    def __init__(self, npc_id: int):
        self.id = npc_id
        
        # -----------------------------
        # AI
        # -----------------------------
        
        self.daily_plan = deque()     # Cola de acciones del día
        self.current_action = None     # Acción en ejecución
        self.last_plan_day = -1

        # --- subsystems ---
        self._stats = NPCStats()
        self.memory = NPCMemory()
        self.social = NPCSocial()
        
        #--------Ubicacion------------
        self.current_location = None

        # Expose flat attributes expected by external code
        # (drives / actions reference npc.hunger, npc.money, etc. directly)
        self._expose_stats()

    # ------------------------------------------------------------------
    # Stats proxy — keeps external API identical to the original class
    # ------------------------------------------------------------------

    def _expose_stats(self):
        """
        Bind stat attributes directly on self so that callers can still
        write  `npc.hunger`, `npc.money`, etc.
        The NPCStats object remains the authoritative store; we simply
        delegate via __getattr__ / __setattr__ overrides below.
        """
        # We store the subsystem under a private name to avoid recursion.
        # All other attribute access falls through to _stats.
        pass

    def __getattr__(self, name):
        # Avoid infinite recursion for private/dunder names
        if name.startswith("_") or name in ("id", "memory", "social"):
            raise AttributeError(name)
        stats = object.__getattribute__(self, "_stats")
        if hasattr(stats, name):
            return getattr(stats, name)
        raise AttributeError(f"'NPC' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith("_") or name in ("id", "memory", "social"):
            object.__setattr__(self, name, value)
            return
        try:
            stats = object.__getattribute__(self, "_stats")
            if hasattr(stats, name):
                setattr(stats, name, value)
                return
        except AttributeError:
            pass
        object.__setattr__(self, name, value)

    # ------------------------------------------------------------------
    # Per-tick update  (called by World)
    # ------------------------------------------------------------------

    def update(self, world):
        
        self._tick_passive()
    
        self.memory.decay()
    
        self._update_plan(world)
    
        execute_plan(self, world)
    
        self._stats.clamp_all()
    
        self.stress += self.city.base_stress * 0.5
    
        self._stats.clamp_all()
                
    
    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _tick_passive(self):
        """Apply time-passing effects before any decision."""
        self._stats.hunger += 1 * self._stats.metabolism
        self._stats.energy -= 2
        self._stats.satiety = max(0, self._stats.satiety - 2)
        self._stats.happiness *= 0.995

    def _update_plan(self, world):
        planner = Planner()
    
        current_day = world.time_manager.day
    
        if self.last_plan_day == current_day:
            return
    
        self.daily_plan = planner.build(
            self,
            world
        )
    
        self.last_plan_day = current_day
    
    