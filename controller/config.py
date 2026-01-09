class Config:
    simulation_name = "Predator: Badlands Simulation"
    grid_width = 20
    grid_height = 20
    cell_size = 25

    initial_deks = 1
    initial_thias = 1
    initial_monsters = 5
    initial_wildlife = 8

    dek_attack_damage = 25
    monster_attack_damage = 15
    wildlife_attack_damage = 5

    move_stamina_cost = 2
    attack_stamina_cost = 5
    carry_stamina_cost = 3
    stamina_regen = 5

    honour_monster_kill = 50
    honour_wildlife_kill = 10
    honour_death_penalty = -30
