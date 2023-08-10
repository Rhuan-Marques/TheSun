import io
import json
import os
import pickle
from typing import Optional, Collection, List

import discord
import rapidfuzz
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from replit import db


from keepalive import keepalive


client = commands.Bot(command_prefix='>', help_command=None, intents=discord.Intents.all())

token = os.environ["token"]

the_world_guild_id = 991948157116219412

# Atualizando as item/location list pro autocomplete
with open("items.json", "rb") as f:
    mw_items_list = json.load(f)
with open("locations.json", "rb") as f:
    mw_locations_list = json.load(f)


mw_emojis = {
    'bk': '<:bk:1077312979068002406>',
    'bobs': '<:bobs:1094744804027535481>',
    'check': '<:check:1077316829019635762>',
    'finished': '<:finished:1110431533518569483>',
}

emojis = {
    # --------------- PROFILE ------------------
    'animal crossing': '<:animal_crossing:995956087503196250>',
    'persona': '<:persona:996145369832497182>',
    'zelda': '<:riki:995956109145817089>',
    'xenoblade': '<:xenoblade:995956105106698310>',
    'mario': '<:mario:995956091210965042>',
    'minecraft': '<:minecraft:995956094679666778>',
    'terraria': '<:terraria:995956102258774026>',
    'metal gear': '<:metal_gear:995956386670321675>',
    'smash bros': '<:smash_bros:995956100140646472>',
    'fire emblem': '<:fire_emblem:995956089097039963>',
    'ace attorney': '<:ace_attorney:996145339021131899>',
    'sonic': '<:sonic:996145390732718181>',
    'the witcher': '<:the_witcher:996151661749882942>',
    'danganronpa': '<:danganronpa:996148242758778950>',
    'visual novels': '<:visual_novels:996150378347384843>',
    "shoot'em ups": '<:shoot_em_ups:996150372420825178>',
    'street fighter': '<:street_fighter:996145396646686820>',
    'rocket league': '<:rocket_league:996145380393754794>',
    'shin megami tensei': '<:shin_megami_tensei:996145388102897714>',
    'touhou': '<:touhou:996145407899992065>',
    'final fantasy': '<:final_fantasy:996145347854352474>',
    'undertale': '<:undertale_deltarune:996158660998873159>',
    'deltarune': '<:undertale_deltarune:996158660998873159>',
    'castlevania': '<:castlevania:996145341504159896>',
    'god of war': '<:god_of_war:996145351696330774>',
    'celeste': '<:celeste:996145343177703565>',
    'halo': '<:halo:996145354774953994>',
    'crash bandicoot': '<:crash_bandicoot:996145345916575835>',
    'stardew valley': '<:stardew_valley:996145394440487014>',
    'kingdom hearts': '<:kingdom_hearts:996145362584731688>',
    'monster hunter': '<:monster_hunter:996145366082789478>',
    'monkey island': '<:monkey_island:996145364149223515>',
    'omori': '<:omori:996145367961845760>',
    'resident evil': '<:resident_evil:996145377965244456>',
    'pokemon': '<:pokemon:996154468406145075>',
    'souls': '<:souls:996146888149581965>',
    'dark souls': '<:souls:996146888149581965>',
    'sekiro': '<:souls:996146888149581965>',
    'bloodborne': '<:souls:996146888149581965>',
    'elden ring': '<:souls:996146888149581965>',
    'the elder scrolls': '<:the_elder_scrolls:996147413939142667>',
    'skyrim': '<:the_elder_scrolls:996147413939142667>',
    'morrowind': '<:the_elder_scrolls:996147413939142667>',
    'gta': '<:rockstar:996145384655171706>',
    'grand theft auto': '<:rockstar:996145384655171706>',
    'red dead redemption': '<:rockstar:996145384655171706>',
    'hollow knight': '<:hollow_knight:996145359921348721>',
    'tekken': '<:tekken:996145400836788344>',
    'baba is you': '<:baba_is_you:996284977585066034>',
    'devil may cry': '<:devil_may_cry:996286578441859102>',
    'fortnite': '<:fortnite:996284980730806352>',
    'little big planet': '<:little_big_planet:996284983360638996>',
    'littlebigplanet': '<:little_big_planet:996284983360638996>',
    'oneshot': '<:oneshot:996284987575910520>',
    'professor layton': '<:professor_layton:996284990994268290>',
    'retro': '<:retro_gaming:996284992781041694>',
    'retro gaming': '<:retro_gaming:996284992781041694>',
    'yakuza': '<:yakuza:996284995494752337>',
    'multiversus': '<:multiversus:999051859232821288>',
    'adventure time': '<:adventure_time:996286966599516170>',
    'arcane': '<:arcane:996286969120301076>',
    'attack on titan': '<:attack_on_titan:996286971095810139>',
    'shingeki no kyojin': '<:attack_on_titan:996286971095810139>',
    'ben10': '<:ben10:996286975571132447>',
    'bleach': '<:bleach:996286978519744512>',
    'breaking bad': '<:breaking_bad:996291500990279720>',
    'dc': '<:dc:996286983913607198>',
    'dc comics': '<:dc:996286983913607198>',
    'death note': '<:death_note:996287357563174952>',
    'dragon ball': '<:dragon_ball:996286989416529971>',
    'dragon prince': '<:dragon_prince:996286993396924490>',
    'how to train your dragon': '<:dragons:996287012317433926>',
    'dragons': '<:dragons:996287012317433926>',
    'eragon': '<:eragon:996286995980627979>',
    'fate': '<:fate:996286998467838042>',
    'fate stay night': '<:fate:996286998467838042>',
    'fullmetal alchemist': '<:fullmetal_alchesmist:996287000271409172>',
    'fullmetal alchemist brotherhood': '<:fullmetal_alchesmist:996287000271409172>',
    'game of thrones': '<:game_of_thrones:996291503053869146>',
    'gintama': '<:gintama:996287005300371456>',
    'gravity falls': '<:gravity_falls:996291506287673414>',
    'harry potter': '<:harry_potter:996287010664886292>',
    'hunter hunter': '<:hunter_hunter:996287014611734620>',
    'hunter x hunter': '<:hunter_hunter:996287014611734620>',
    'kill la kill': '<:kill_la_kill:996287018583732374>',
    'konosuba': '<:konosuba:996291508049301526>',
    'kono subarashii sekai ni shukufuku o': '<:konosuba:996291508049301526>',
    'lovecraft': '<:lovecraft:996287022455074897>',
    'puella magi madoka magica': '<:madoka:996291510872068146>',
    'madoka magica': '<:madoka:996291510872068146>',
    'marvel': '<:marvel:996287029673467965>',
    'marvel cinematic universe': '<:marvel:996287029673467965>',
    'mcu': '<:marvel:996287029673467965>',
    'monogatari': '<:monogatari:996287033439944744>',
    'my hero academia': '<:my_hero_academia:996287035881050172>',
    'boku no hero academia': '<:my_hero_academia:996287035881050172>',
    'boku no hero': '<:my_hero_academia:996287035881050172>',
    'my little pony': '<:my_little_pony:996287038498287616>',
    'naruto': '<:naruto:996287040708677782>',
    'one piece': '<:one_piece:996287044844269658>',
    'owl house': '<:owl_house:996287047176310846>',
    'the owl house': '<:owl_house:996287047176310846>',
    'rick and morty': '<:rick_and_morty:996287050338811915>',
    'star vs the forces of evil': '<:star_vs_the_forces_of_evil:996287052423368744>',
    'star vs': '<:star_vs_the_forces_of_evil:996287052423368744>',
    'star': '<:star_vs_the_forces_of_evil:996287052423368744>',
    'star wars': '<:star_wars:996287055258718289>',
    'mandalorian': '<:star_wars:996287055258718289>',
    'steins gate': '<:steins_gate:996287057464938596>',
    'steins;gate': '<:steins_gate:996287057464938596>',
    'steven universe': '<:steven_universe:996287059239125082>',
    'steven': '<:steven_universe:996287059239125082>',
    'stranger things': '<:stranger_things:996287060975570994>',
    'studio ghibli': '<:studio_ghibli:996291514831491072>',
    'ghibli': '<:studio_ghibli:996291514831491072>',
    'tales of arcadia': '<:tales_of_arcadia:996305722541363200>',
    'trollhunters': '<:tales_of_arcadia:996305722541363200>',
    'tolkien': '<:tolkien:996287072748965998>',
    'lord of the rings': '<:tolkien:996287072748965998>',
    'hobbit': '<:tolkien:996287072748965998>',
}


mw_item_cache = []
mw_world_names_cache = {}
async def update_mw_cache():

    with open('status.bin', 'rb') as file:
        worlds = pickle.load(file)

    new_item_cache = []
    new_world_name_cache = {}
    for world in worlds:
        new_item_cache.extend(world['items'])
        new_world_name_cache[world['world_name']] = world['author_id']

    global mw_item_cache
    global mw_world_names_cache
    mw_item_cache = new_item_cache
    mw_world_names_cache = new_world_name_cache
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(f'Rikis = {db["riki"]}')
    await update_mw_cache()

@client.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para utilizar esse comando")
    else:
        raise error


@client.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    try:
        synced = await client.tree.sync()
        await ctx.send(f'Synced {len(synced)} commands')
    except Exception as e:
        await ctx.send(f'ERROR: {e}')

# Função pra adms poderem usar dar like/unlike/etc pros outros.
# ENTRADA: um ctx e uma string (entrada de outra função)
# SAÍDA: um membro (mencionado) e uma string (entrada sem a menção)
async def adm_tag_check(ctx, full_string):
    if len(ctx.message.mentions) > 0:
        if ctx.message.author.guild_permissions.administrator:
            member = ctx.message.mentions[0]
            full_string = full_string.replace(ctx.message.mentions[0].mention, "")
        else:
            await ctx.send("KK O CARA TENTA COMANDAR PROFILE DOS OUTRO SEM SER ADM")
            member = ctx.author
        full_string = full_string.strip()
    else:
        member = ctx.author
    print(full_string)
    return full_string, member


# ---------------------- MULTIWORLD -----------------------------
# Função que atualiza o status do MW no canal adequado
# RESULTADO: Apaga e remanda a mensagem de status com a informação atualizada do status.bin
async def update_status():
    #  1077326271924678769
    channel = client.get_channel(1094747665675337828)
    previous_message = [message async for message in channel.history(limit=2)]
    if previous_message:
        await previous_message[-1].delete()
    message = ""
    with open('status.bin', 'rb') as file:
        worlds = pickle.load(file)
    for world in worlds:
        emoji = world['emoji']
        world_name = world['world_name']
        items = world['items']
        locations = world['locations']
        message += f"{emoji} **{world_name}**"
        print(f'items:{items} locations{locations}')
        if items or locations:
            message += " -- "
        if items:
            message += ", ".join(items)
        if locations:
            if items:
                message += " "
            message += "(" + ", ".join(locations) + ")"
        message += "\n"

    await update_mw_cache()

    await channel.send(message)


@client.hybrid_command()
@app_commands.guild_only
# Comando pra entrar no MW
# ENTRADA: 1 ou mais .yamls e world_name (opcional e só se for um unico yaml)
# RESULTADO: yamls mandados ao canal correto, player adicionado a status.bin
async def start(ctx: commands.Context, world1: discord.Attachment,
                world2: Optional[discord.Attachment],
                world3: Optional[discord.Attachment],
                world4: Optional[discord.Attachment],
                world5: Optional[discord.Attachment],
                world_name: Optional[str]):

    await ctx.defer()
    non_none_attachments = filter(None, [world1, world2, world3, world4, world5])
    yaml_attachments = list(filter(lambda attch: attch.filename.endswith('.yaml'), non_none_attachments))

    author_id = str(ctx.author.id)

    if len(yaml_attachments) > 1 and world_name:
        await ctx.send("Mande somente um .yaml por vez para colocar World Names manualmente")
    elif len(yaml_attachments) > 0:
        # Pega a antiga lista de mundos
        with open('status.bin', 'rb') as file:
            data = file.read()
        if data:
            worlds = pickle.load(io.BytesIO(data))
        else:
            worlds = []
        for attachment in yaml_attachments:
            yaml_content = await attachment.read()
            if not world_name:
                world_name = attachment.filename.split(".")[0]
            # the world:  1077113732485894244
            channel = client.get_channel(1094748488341921865)
            await channel.send(file=discord.File(io.BytesIO(yaml_content), filename=world_name + ".yaml"))
            worlds.append({
                'author_id': author_id,
                'world_name': world_name,
                'emoji': mw_emojis['check'],
                'items': [],
                'locations': []
            })
            world_name = ''
        with open('status.bin', 'wb') as file:
            pickle.dump(worlds, file)
        await ctx.send("Os seus .yaml foram enviados")
        await update_status()
    else:
        await ctx.send("Mande seu .yaml")

    await ctx.message.delete()

@start.error
async def start_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Placeholder pra mensagem, por favor não esquecer de arrumar")

@client.hybrid_command()
@app_commands.default_permissions()
@commands.has_permissions(administrator=True)
# Comando de adm pra atualizar o status
# RESULTADO: chama update_status
async def reset(ctx: commands.Context):
    if os.path.isfile("status.bin"):
        os.remove("status.bin")
        await ctx.send("Instancia apagada!")
    else:
        await ctx.send("Erro: Não tem uma instância de Multiworld no momento!")

@client.hybrid_command()
@app_commands.default_permissions()
@commands.has_permissions(administrator=True)
# Comando de adm pra atualizar o status
# RESULTADO: chama update_status
async def devupdate(ctx: commands.Context):
    await ctx.defer()
    await update_status()
    await ctx.send("Status atualizado com sucesso!", ephemeral=True)


async def generic_fuzzy_autocomplete(current: str, choices: Collection, limit: int = 10) -> List[Choice[str]]:
    return [Choice(name=result, value=result)
            for result, _, _ in rapidfuzz.process.extract(current, choices, limit=limit)]


async def items_autocomplete(interaction: discord.Interaction, current: str):
    return await generic_fuzzy_autocomplete(current, mw_items_list, limit=5)


async def locations_autocomplete(interaction: discord.Interaction, current: str):
    return await generic_fuzzy_autocomplete(current, mw_locations_list, limit=5)


async def get_items_autocomplete(interaction: discord.Interaction, current: str):
    return await generic_fuzzy_autocomplete(current, mw_item_cache)

async def world_names_autocomplete(interaction: discord.Interaction, current: str):
    return [Choice(name=world_name, value=world_name)
            for world_name, _, _ in rapidfuzz.process.extract(current, mw_world_names_cache.keys())
            if interaction.user.id == int(mw_world_names_cache[world_name])]


@client.hybrid_command()
@app_commands.guild_only
@app_commands.autocomplete(
    world_name=world_names_autocomplete,
    item1=items_autocomplete,
    item2=items_autocomplete,
    item3=items_autocomplete,
    item4=items_autocomplete,
    location1=locations_autocomplete,
    location2=locations_autocomplete,
    location3=locations_autocomplete,
    location4=locations_autocomplete,
)
async def bk(ctx, world_name: Optional[str],
             item1: Optional[str],
             location1: Optional[str],
             item2: Optional[str],
             location2: Optional[str],
             item3: Optional[str],
             location3: Optional[str],
             item4: Optional[str],
             location4: Optional[str]):
    await change_state(ctx, 'bk', world_name, item1, location1, item2, location2, item3, location3, item4, location4)

@client.hybrid_command()
@app_commands.guild_only
@app_commands.autocomplete(
    world_name=world_names_autocomplete,
    item1=items_autocomplete,
    item2=items_autocomplete,
    item3=items_autocomplete,
    item4=items_autocomplete,
    location1=locations_autocomplete,
    location2=locations_autocomplete,
    location3=locations_autocomplete,
    location4=locations_autocomplete,
)

async def bobs(ctx, world_name: Optional[str],
             item1: Optional[str],
             location1: Optional[str],
             item2: Optional[str],
             location2: Optional[str],
             item3: Optional[str],
             location3: Optional[str],
             item4: Optional[str],
             location4: Optional[str]):
    await change_state(ctx, 'bobs', world_name, item1, location1, item2, location2, item3, location3, item4, location4)

@client.hybrid_command()
@app_commands.guild_only
@app_commands.autocomplete(
    world_name=world_names_autocomplete,
)
async def finish(ctx, world_name: Optional[str]):
  await change_state(ctx, 'finished', world_name, '', '', '', '', '', '', '', '')

@client.hybrid_command()
@app_commands.guild_only
@app_commands.autocomplete(
    world_name=world_names_autocomplete,
)
async def free(ctx, world_name: Optional[str]):
  await change_state(ctx, 'check', world_name, '', '', '', '', '', '', '', '')
"""
async def clear_itens(ctx, world_name: Optional[str]):
  world = get_world(ctx, world_name)
  if type(world == dict):
    world['items'].clear()
    world['locations'].clear()
    with open('status.bin', 'wb') as file:
        pickle.dump(worlds, file)

    await update_status()
    

async def get_world(ctx, world_name: Optional[str]):
    with open('status.bin', 'rb') as file:
        worlds = pickle.load(file)
    matching_worlds = [world for world in worlds if world_name == world['world_name']]
    user_worlds = [world for world in worlds if world['author_id'] == str(ctx.author.id)]

    if len(matching_worlds) > 0:
        world = matching_worlds[0]
        return world
    elif len(user_worlds) == 1:
        world = user_worlds[0]
        return world
    elif len(user_worlds) == 0:
        if not world_name:
            return -1
            
        else:
            return -2
        return
    elif not world_name:
        return -3
    else:
        return -4
    return world
"""

async def change_state(ctx, emoji: str,
             world_name: Optional[str],
             item1: Optional[str],
             location1: Optional[str],
             item2: Optional[str],
             location2: Optional[str],
             item3: Optional[str],
             location3: Optional[str],
             item4: Optional[str],
             location4: Optional[str]):
    """
    world = await get_world(ctx, world_name)
    if type(world) != dict:
      if world == -1:
        await ctx.send('Você não tem um mundo.')
      elif world == -2:
        await ctx.send(f'Mundo {world_name} não existe')
      elif world == -3:
        await ctx.send('Você tem mais de um mundo, expecifique qual deseja.')
      elif world == -4:
        await ctx.send(f'Mundo {world_name} não existe, tente novamente.')
      else:
        await ctx.send(f'HUMMMM {type(world)}')
      return
    
    world_name = world['world_name']
    """
    with open('status.bin', 'rb') as file:
        worlds = pickle.load(file)
    matching_worlds = [world for world in worlds if world_name == world['world_name']]
    user_worlds = [world for world in worlds if world['author_id'] == str(ctx.author.id)]

    if len(matching_worlds) > 0:
        world = matching_worlds[0]
    elif len(user_worlds) == 1:
        world = user_worlds[0]
        world_name = world['world_name']
    elif len(user_worlds) == 0:
        if not world_name:
            await ctx.send('Você não tem um mundo.')
        else:
            await ctx.send(f'Mundo {world_name} não existe')
        return
    elif not world_name:
        await ctx.send('Você tem mais de um mundo, expecifique qual deseja.')
        return
    else:
        await ctx.send(f'Mundo {world_name} não existe, tente novamente.')
        return

    items = list(filter(None, [item1, item2, item3, item4]))
    locations = list(filter(None, [location1, location2, location3, location4]))
    world['emoji'] = mw_emojis[emoji]
    world['items'].extend(items)
    world['locations'].extend(locations)
    message = f'{world_name} agora está em {world["emoji"]}'
    if items:
        message += ' até que peguem'
        message += ''.join([f' {item} ou' for item in items])
        message = message.rstrip(' ou')
    if locations:
        message += ' nos locais'
        message += ''.join([f' {location} ou' for location in locations])
        message = message.rstrip(' ou')
    await ctx.send(message)
    with open('status.bin', 'wb') as file:
        pickle.dump(worlds, file)

    await update_status()


@client.hybrid_command()
@app_commands.guild_only
@app_commands.autocomplete(
    item1=get_items_autocomplete,
    item2=get_items_autocomplete,
    item3=get_items_autocomplete,
    item4=get_items_autocomplete)
# Comando pra pegar item de alguem que precisa
# ENTRADA: Lista de items (por enquanto em uma unica string separados por /)
# RESULTADO: Procura se alguem precisa destes itens e deixa-os livres.
async def get(ctx,
              item1: str,
              item2: Optional[str],
              item3: Optional[str],
              item4: Optional[str],):
    await ctx.defer()

    items = list(filter(None, [item1, item2, item3, item4]))

    with open('status.bin', 'rb') as file:
        worlds = pickle.load(file)
    for world in worlds:
        for item in items:
            print(item in world['items'])
            if item in world['items']:
                print("cheguei")
                await ctx.send(f'{item} mandado para {world["world_name"]}\nElu não está mais {world["emoji"]}')
                world['items'] = []
                world['locations'] = []
                world['emoji'] = mw_emojis['check']

    with open('status.bin', 'wb') as file:
        pickle.dump(worlds, file)
    await update_status()


@get.error
async def get_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Você tem que especificar o item coletado.", ephemeral=True)

# Comando pra liberar alguem
# ENTRADA: Nome de um mundo
# RESULTADO: Deixa o mundo Free e sem precisar de nenhum item e/ou location

# ---------------------- PROFILES -----------------------------


async def medias_autocomplete(interaction: discord.Interaction, current: str):
    return [Choice(name=media_name, value=media_name)
            for media_name, i1, i2 in rapidfuzz.process.extract(current, emojis.keys())]


@client.hybrid_command(name="like")
@app_commands.guild_only
@app_commands.autocomplete(media1=medias_autocomplete,
                           media2=medias_autocomplete,
                           media3=medias_autocomplete,
                           media4=medias_autocomplete)
async def like(ctx,
               media1: str,
               media2: Optional[str],
               media3: Optional[str],
               media4: Optional[str]):
    """
    You can define what you like*, using like.

    o like multiple things at once, use *commas and space* between them.
    **Example:** *like minecraft, castlevania, The Titanic, sleeping late

    Some of the things you like might be in our Medias Database, and will be transformed in emojis in a special section of your profile. The others will be shown below, in text, exactly how you sent.
    >unlike can be used in the same way to things from your like list
    unlike all will clear it completely
    To view all of the Medias Database, use !medias')

    """
    # if full_string == '':
    #     await ctx.send(
    #         'No media received.\n\nCorrect syntax: !like *<media 1>*, *<media 2>*, *<media 3>*, etc\n\nMore info in !help like')
    #     return
    await ctx.defer()

    # Corrigindo a incapacidade dos argumentos padrões de separarem os argumentos
    if ctx.interaction is None:
        string_separator = " "
    else:
        string_separator = ", "

    # Junta as medias em uma string, ignorando None, pra passar pro código legado
    full_string = string_separator.join(filter(None, [media1, media2, media3, media4]))

    full_string, member_obj = await adm_tag_check(ctx, full_string)
    member = str(member_obj.id)
    if member + '|&|likes' not in db.keys():
        like = []
        db[member] = member_obj.display_name
        db[member + '|&|likes'] = like
        db[member + '|&|likes too'] = like
    media_list = full_string.split(', ')
    strin = 'You now like: '
    strin2 = 'You now like '
    strinf = ''
    first = True
    for media in media_list:
        if media.lower() in emojis:
            media = emojis[media.lower()]
            if media not in db[member + '|&|likes']:
                db[member + '|&|likes'].append(media)
                strin += (media + ' ')
            else:
                strin += media + '(already liked) '
        else:
            if media.startswith('/string '):
                media = media.replace('/string ', '')
            db[member + '|&|likes too'].append(media)
            if first == True:
                first = False
            else:
                strin2 += ', '
            strin2 += media
    if strin != 'You now like: ':
        strinf += strin
    strinf += '\n'
    if strin2 != 'You now like ':
        strinf += strin2 + ' too'
    await ctx.send(strinf)


@like.error
async def like_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("""No media received.
        Correct syntax: !like *<media 1>*, *<media 2>*, *<media 3>*, etc
        More info in !help like""")


@client.hybrid_command(name="unlike")
@app_commands.guild_only
@app_commands.autocomplete(media1=medias_autocomplete,
                           media2=medias_autocomplete,
                           media3=medias_autocomplete,
                           media4=medias_autocomplete)
async def unlike(ctx,
                 media1: str,
                 media2: Optional[str],
                 media3: Optional[str],
                 media4: Optional[str]):
     
    if ctx.interaction is None:
        string_separator = " "
    else:
        string_separator = ", "

    # Junta as medias em uma string, ignorando None, pra passar pro código legado
    full_string = string_separator.join(filter(None, [media1, media2, media3, media4]))

    full_string, member = await adm_tag_check(ctx, full_string)
    member = str(member.id)
    if member + '|&|likes' not in db.keys():
        await ctx.send('You do not have liked a thing.\n!like to begin it')
        return
    if full_string.lower() == 'all':
        db[member + '|&|likes'].clear()
        db[member + '|&|likes too'].clear()
        await ctx.send('Everything has been unliked.\nGood luck on your sad life...')
        return
    media_list = full_string.split(', ')
    strin = ''
    strin2 = ''
    strinFail = ''
    strinFinal = ''
    first = True
    firstFail = True
    for media in media_list:
        if media.lower() in emojis:
            media = emojis[media.lower()]
            if media in db[member + '|&|likes']:
                db[member + '|&|likes'].remove(media)
                strin += media + ' '
            else:
                if firstFail == False:
                    strinFail += ', '
                strinFail += media
                firstFail = False
        elif media.lower() in mw_emojis:  # Done to un-do softlocks
            media = mw_emojis[media.lower()]
            db[member + '|&|likes'].remove(media)
            strin += media + ' '
            if first == False:
                strin += ', '
            else:
                first = False
        else:
            if media.startswith('/string '):
                media = media.replace('/string ', '')
            if media in db[member + '|&|likes too']:
                db[member + '|&|likes too'].remove(media)
                if first == False:
                    strin2 += ', '
                strin2 += media
                first = False
            else:
                if firstFail == False:
                    strinFail += ', '
                strinFail += media
                firstFail = False
    if strin != '':
        strinFinal += f'You dont like {strin} anymore'
    if strin2 != '':
        strinFinal += f'\nYou dont like {strin2} anymore'
        if strin != '':
            strinFinal += ' either'
    if strinFail != '':
        strinFinal += f'\nSeems like you didnt even like {strinFail} in the first place'
    await ctx.send(strinFinal)


@unlike.error
async def unlike_error(ctx: commands.Context, error: commands.CommandError):
  """You can unlike what you liked using like.

        To like multiple things at once, use *commas and space* between them.
        **Example:** *like minecraft, castlevania, The Titanic, sleeping late

        Some of the things you like might be in our Medias Database, and will be transformed in emojis in a special section of your profile. The others will be shown below, in text, exactly how you sent.
        >unlike can be used in the same way to things from your like list
        unlike all will clear it completely
        To view all of the Medias Database, use !medias')
    """
  if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("""No media received.
        Correct syntax: !like *<media 1>*, *<media 2>*, *<media 3>*, etc
        More info in !help like""")


@client.command()
async def deleteprofile(ctx, *, full_string=''):
    full_string, member = await adm_tag_check(ctx, full_string)
    member = str(member.id)
    if member not in db.keys():
        await ctx.send('You do not have a profile.\n')
        return
    del db[member]
    del db[member + '|&|likes']
    del db[member + '|&|likes too']
    del db[member + '|&|id']
    await ctx.send(f'Your profile ({member}) was deleted')


@client.hybrid_command()
@app_commands.guild_only
@app_commands.describe(membro="Membro dono do perfil")
async def profile(ctx, membro: Optional[discord.Member]):
    """
    A profile can hold information about medias you like and your accounts and ids

    To view someones profile use >profile @person
    To delete your own profile use >deleteprofile
    To know more about likes, see !help like
    To know more about Accounts and Ids, see !help gameid')
"""
    if membro is None:  # Seta o padrão pra ser o autor da msgm
        membro = ctx.author
    member = str(membro.id)  # Separa member (str) e membro (User)
    if member not in db.keys():
        await ctx.send(f'{membro.display_name} ainda não tem um Profile.\n')
    else:
        await ctx.send(f"**----- {membro.display_name}'s Profile:** -----")
        if member + '|&|id' in db.keys() and db[member + '|&|id']:  # Checka se tem id registrado
            dict = db[member + '|&|id']
            strin = ''
            for key in dict:
                strin += key + ': ' + dict[key] + '\n'  # "[Plataform]: [Account]"
            await ctx.send(f'{membro.display_name} **Accounts** and **IDs**:\n{strin}')
        if member + '|&|likes' in db.keys() and db[member + '|&|likes']:
            lista = db[member + '|&|likes']
            strin = ''
            for x in lista:
                strin = strin + x + ' '
            await ctx.send(f'**{membro.display_name} likes:**\n{strin}')
        if member + '|&|likes too' in db.keys() and db[member + '|&|likes too']:
            lista = db[member + '|&|likes too']
            strin = ''
            for x in lista:
                strin = strin + x + '\n'
            await ctx.send(f'**{membro.display_name} also likes:**\n{strin}')


@profile.error
async def profile_error(ctx: commands.Context, error: commands.CommandError):
    pass


@client.hybrid_command()
@app_commands.guild_only
async def medias(ctx):
    """
    The Medias Database is the list of things you can >like and will be turned into an special emoji

    You can use >medias to see them all or test it for yourself.

    """
    full_line = ['']  # Determinado como lista pra usar depois
    full_line[0] = 'All medias that you can "Like" are:\n'  # Adiciona direto na string, menos trabalho
    i = 0
    emoji_atual = ''
    for media in emojis:
        if emoji_atual != emojis[media]:  # check pra nao exibir emoji repetido, gerado por aliases
            emoji_atual = emojis[media]
            full_line[i] += emoji_atual + ' '
            if len(full_line[i]) > 1650:  # Limite do discord de 2000 caracteres
                full_line.append('')
                i += 1
    for message in full_line:
        await ctx.send(message)
    await ctx.send(
        '\n\nRemember you can always !like something not in this list and it will appear in you "Like too" section, right below your "Liked" ones')


@client.hybrid_command()
@app_commands.guild_only
async def gameid(ctx, game: str, id: str):
    """
    '>gameid can be used to put your **Accounts** and **IDs** in your profile

    **Example:** !gameid steam, TheSun\
    If you want to remove it, you can by using:
    >gameid steam, remove

    Be aware that as the command require multiple inputs, you **cannot add multiple accounts at once**')
    """
    # if full_string == '':
    #     await ctx.send(
    #         'No Game nor ID received.\n\nCorrect syntax: !gameid *<platform or game>*, *<nick or id>*\n\nMore info in !help gameid')
    #     return
    member = str(ctx.author.id)

    if member + '|&|id' not in db.keys():
        db[member] = ctx.author.display_name
        aux = {}
        db[member + '|&|id'] = aux
    if (game.lower() == 'steam'):
        if id == 'remove':
            del db[member + '|&|id']['<:steam:996219593163034674>']
            await ctx.send(f'Your <:steam:996219593163034674> Account has been removed')
        else:
            db[member + '|&|id']['<:steam:996219593163034674>'] = id
            await ctx.send(f'Your <:steam:996219593163034674> Account is now: {id}')
    elif game.lower() in {'psn', 'playstation network', 'playstation online'}:
        if id == 'remove':
            del db[member + '|&|id']['<:playstation:996219591606935572>']
            await ctx.send(f'Your <:playstation:996219591606935572> Account has been removed')
        else:
            db[member + '|&|id']['<:playstation:996219591606935572>'] = id
            await ctx.send(f'Your <:playstation:996219591606935572> Account is now: {id}')
    elif game.lower() in {'xbox', 'xbox online', 'microsoft', 'microsoft account'}:
        if id == 'remove':
            del db[member + '|&|id']['<:xbox:996219599529971743>']
            await ctx.send(f'Your <:xbox:996219599529971743> Account has been removed')
        else:
            db[member + '|&|id']['<:xbox:996219599529971743>'] = id
            await ctx.send(f'Your <:xbox:996219599529971743> Account is now: {id}')
    elif game.lower() in {'nintendo switch', 'nintendo switch online', 'nso', 'switch online', 'switch', 'nintendo'}:
        if id == 'remove':
            del db[member + '|&|id']['<:switch:996219594723311707>']
            await ctx.send(f'Your <:switch:996219594723311707> Account has been removed')
        else:
            db[member + '|&|id']['<:switch:996219594723311707>'] = id
            await ctx.send(f'Your <:switch:996219594723311707> Account is now: {id}')
    elif game.lower() in {'anilist'}:
        if id == 'remove':
            del db[member + '|&|id']['<:anilist:1001303751178596502>']
            await ctx.send(f'Your <:anilist:1001303751178596502> Account has been removed')
        else:
            db[member + '|&|id']['<:anilist:1001303751178596502>'] = id
            await ctx.send(f'Your <:anilist:1001303751178596502> Account is now: {id}')
    elif game.lower() in {'backloggd', 'backlogged', 'backlogd', 'backloged'}:
        if id == 'remove':
            del db[member + '|&|id']['<:backloggd:1003801290201116702>']
            await ctx.send(f'Your <:backloggd:1003801290201116702> Account has been removed')
        else:
            db[member + '|&|id']['<:backloggd:1003801290201116702>'] = id
            await ctx.send(f'Your <:backloggd:1003801290201116702> Account is now: {id}')
    else:
        if game.startswith('/string '):
            game = game.replace('/string ', '')
        if id == 'remove':
            if game in db[member + '|&|id']:
                del db[member + '|&|id'][game]
                await ctx.send(f'Your {game} has been removed')
            else:
                await ctx.send(f'You did not have a {game} Account')
            return
        else:
            db[member + '|&|id'][game] = id
            await ctx.send(f'Your {game} Account is now: {id}')


@gameid.error
async def gameid_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("""No Game nor ID received.
        Correct syntax: !gameid *<platform or game>*, *<nick or id>*
        More info in !help gameid""")


# ---------------------- OTHER -----------------------------
@client.hybrid_command()
@app_commands.guild_only
async def cv(ctx, rate: float, dmg: float):
    """
    Comando pra calcular Crit Value de genshin

    ENTRADA: Dois floats
    RESULTADO: Printa resultado
    """
    await ctx.send(f'Rate = {rate}\nDmg = {dmg}\n**Value = {rate * 2 + dmg}**')


@cv.error
async def cv_error(ctx: commands.Context, error: commands.CommandError):
    pass


@client.hybrid_command()
@commands.has_role(1078785836750999693)
@app_commands.guild_only
@app_commands.describe(hex_code="Código da cor")
# Comando pra mudar cor do cargo Pizza
# ENTRADA: HexCode equivalente a cor
# RESULTADO: Muda cor do cargo
async def color(ctx, hex_code: discord.Color):
    # Check if user has role "The Brush"
    role = discord.utils.get(ctx.guild.roles, id=1078785836750999693)

    # # Check if hex code is valid
    # try:
    #     new_color = hex_code
    # except ValueError:
    #     await ctx.send("Isso não é um Hex Code")
    #     return

    # Change color of role
    await role.edit(color=hex_code)
    await ctx.send(f"Sua cor foi mudada pra: {hex_code}!")


@color.error
async def color_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Você não tem o cargo certo pra usar esse comando")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Coloque o código da cor")
    elif isinstance(error, commands.ConversionError):
        await ctx.send("Cor inválida")
    elif isinstance(error, commands.BadColorArgument):
        await ctx.send("Código da cor inválido")


@client.command()
# Comando pra adicionar personagens ao cringe_contestants.txt
# ENTRADA: uma string
# RESULTADO: String e autor adicionados a cringe_contestants.txt
async def cringe(ctx, *, line):
    author_name = ctx.author.name
    author_id = ctx.author.id
    output = f"{author_name} - {author_id} - {line}"
    # Open file in append mode and write line to it
    with open("cringe_contestants.txt", "a") as f:
        f.write(output + "\n")

    await ctx.send(f"{line} foi adicionado as ideias de concorrentes para o próximo #cringe.")


@client.command()
# Bem vindo ao HELP wall of text
async def help(ctx, arg=''):
    arg = arg.replace('!', '')
    arg = arg.replace('<', '')
    arg = arg.replace('>', '')
    if arg.lower() == 'profile':
        await ctx.send(
            'A profile can hold information about **medias you like** and your **accounts and ids**\n\nTo view someones profile use >profile @person\n\nTo delete your own profile use >deleteprofile\n\nTo know more about likes, see !help like\n\nTo know more about Accounts and Ids, see !help gameid')
    elif arg.lower() in {'like', 'unlike'}:
        await ctx.send(
            'You can define what you **like**, using *like.\nTo like multiple things at once, use *commas and space* between them.\n\n**Exemple:** *like minecraft, castlevania, The Titanic, sleeping late\n\nSome of the things you like might be in our Medias Database, and will be transformed in emojis in a special section of your profile. The others will be shown below, in text, exactly how you sent.\n>unlike can be used in the same way to things from your like list\n>unlike all will clear it completely\n\nTo view all of the Medias Database, use !medias')
    elif arg.lower() == 'gameid':
        await ctx.send(
            '>gameid can be used to put your **Accounts** and **IDs** in your profile\n\n**Exemple:** !gameid steam, TheSun\n\nIf you want to remove it, you can by using:\n>gameid steam, remove\n\nBe aware that as the command require multiple inputs, you **cannot add multiple accounts at once**')
    elif arg.lower() == 'medias':
        await ctx.send(
            'The Medias Database is the list of things you can >like and will be turned into an special emoji in your profile\n\nYou can use >medias to see them all or test it for yourself.')
    elif arg.lower() == 'cringe':
        await ctx.send(
            'Send in a character name, preferably with its series next to it, to put it on a list for possible #cringe contestants on future events.\nFor those who don\'t know, #cringe is a tournament of Waifus/Husbandos in the gaming world')
    else:
        await ctx.send(
            '**The Sun Commands:**\n\n**>help** <command> to get more details about that command\n**>profile** to see your profile, with IDs and Likes. Tag someone to see theirs.\n**>like** and **>unlike** to manage your liked medias.\n**>gameid** to add your IDs or Nicks in platforms like Steam, PSN or games\n**>cringe** can be used to give idea for future contestants on #cringe competitivites')


@client.hybrid_command()
@commands.has_permissions(administrator=True)
# Comando de purge
async def purge(ctx, size: int):
    await ctx.defer()
    await ctx.channel.purge(limit=size + 1)
    if (size < 15):
        purge_message = await ctx.send("<:purge:1000627830532608020> MONADO P")
        for i in range(size):
            await purge_message.edit(content=purge_message.content + "U")
            purge_message.content += "U"
        await purge_message.edit(content=purge_message.content + "RGE <:purge:1000627830532608020>")
    elif size < 100:
        purge_message = "<:purge:1000627830532608020> " * int(size / 20 + 1)
        purge_message += "MONADO P"
        purge_message += "U" * size
        purge_message += "RGE "
        purge_message += "<:purge:1000627830532608020> " * int(size / 20 + 1)
        await ctx.send(purge_message)
    else:
        purge_message = "<:purge:1000627830532608020> M <:purge:1000627830532608020> O <:purge:1000627830532608020> N <:purge:1000627830532608020> A <:purge:1000627830532608020> D <:purge:1000627830532608020> O <:purge:1000627830532608020> <:purge:1000627830532608020> <:purge:1000627830532608020> P <:purge:1000627830532608020> U <:purge:1000627830532608020> R <:purge:1000627830532608020> G <:purge:1000627830532608020> E <:purge:1000627830532608020>"
        await ctx.send(purge_message)


@client.command()
@commands.has_permissions(administrator=True)
# Comando de adm pra mandar mensagem pelo bot
async def devsay(ctx, *, line):
    await ctx.send(line)
    ctx.message.delete()


# -- RIKI


# ---------------------- RIKI -----------------------------

@client.hybrid_command()
async def submit(ctx, based_char: str):
    author_name = ctx.author.name
    author_id = ctx.author.id
    output = f"{author_name} - {author_id} - {based_char}"
    # Open file in append mode and write line to it
    with open("based_contestants.txt", "a") as f:
        f.write(output + "\n")

    await ctx.send(f"{based_char} foi votado para o #based")

client.run(token)
keepalive()
