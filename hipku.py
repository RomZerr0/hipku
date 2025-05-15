
import re

class Hipku:
    """
    Hipku version 0.0.2
    Copyright (c) Gabriel Martin 2014
    All rights reserved
    Available under the MIT license
    http://gabrielmartin.net/projects/hipku
    """

    @staticmethod
    def encode(ip):
        ipv6 = Hipku.ip_is_ipv6(ip)
        decimal_octet_array = Hipku.split_ip(ip, ipv6)
        factored_octet_array = Hipku.factor_octets(decimal_octet_array, ipv6)
        encoded_word_array = Hipku.encode_words(factored_octet_array, ipv6)
        haiku_text = Hipku.write_haiku(encoded_word_array, ipv6)
        return haiku_text

    @staticmethod
    def decode(haiku):
        word_array = Hipku.split_haiku(haiku)
        ipv6 = Hipku.haiku_is_ipv6(word_array)
        factor_array = Hipku.get_factors(word_array, ipv6)
        octet_array = Hipku.get_octets(factor_array, ipv6)
        ip_string = Hipku.get_ip_string(octet_array, ipv6)
        return ip_string

    # Helper functions for encoding
    @staticmethod
    def ip_is_ipv6(ip):
        if ':' in ip:
            return True
        elif '.' in ip:
            return False
        else:
            raise ValueError('Formatting error in IP Address input. Contains neither ":" or "."')

    @staticmethod
    def split_ip(ip, ipv6):
        octet_array = []
        decimal_octet_array = []
        v6_base = 16

        if ipv6:
            separator = ':'
            num_octets = 8
        else:
            separator = '.'
            num_octets = 4

        # Remove newline and space characters
        ip = re.sub(r'[\n\ ]', '', ip)
        octet_array = ip.split(separator)

        # If IPv6 address is in abbreviated format, we need to replace missing octets with 0
        if len(octet_array) < num_octets:
            if ipv6:
                num_missing_octets = (num_octets - len(octet_array))
                octet_array = Hipku.pad_octets(octet_array, num_missing_octets)
            else:
                raise ValueError('Formatting error in IP Address input. IPv4 address has fewer than 4 octets.')

        # Convert IPv6 addresses from hex to decimal
        if ipv6:
            for i in range(len(octet_array)):
                decimal_octet_array.append(int(octet_array[i], v6_base))
        else:
            decimal_octet_array = [int(octet) for octet in octet_array]

        return decimal_octet_array

    @staticmethod
    def pad_octets(octet_array, num_missing_octets):
        padded_octet = 0
        a_length = len(octet_array)

        # If the first or last octets are blank, zero them
        if octet_array[0] == '':
            octet_array[0] = str(padded_octet)
        if octet_array[a_length - 1] == '':
            octet_array[a_length - 1] = str(padded_octet)

        # Check the rest of the array for blank octets and pad as needed
        i = 0
        while i < a_length:
            if octet_array[i] == '':
                octet_array[i] = str(padded_octet)
                for j in range(num_missing_octets):
                    octet_array.insert(i, str(padded_octet))
                a_length = len(octet_array)
            i += 1

        return octet_array

    @staticmethod
    def factor_octets(octet_array, ipv6):
        factored_octet_array = []

        if ipv6:
            divisor = 256
        else:
            divisor = 16

        for octet_value in octet_array:
            factor1 = octet_value % divisor
            octet_value = octet_value - factor1
            factor2 = octet_value // divisor

            factored_octet_array.append(factor2)
            factored_octet_array.append(factor1)

        return factored_octet_array

    @staticmethod
    def encode_words(factor_array, ipv6):
        encoded_word_array = []
        key = Hipku.get_key(ipv6)

        for i in range(len(factor_array)):
            dictionary = key[i]
            encoded_word_array.append(dictionary[factor_array[i]])

        return encoded_word_array

    @staticmethod
    def get_key(ipv6):
        if ipv6:
            key = [
                adjectives,
                nouns,
                adjectives,
                nouns,
                verbs,
                adjectives,
                adjectives,
                adjectives,
                adjectives,
                adjectives,
                nouns,
                adjectives,
                nouns,
                verbs,
                adjectives,
                nouns
            ]
        else:
            key = [
                animalAdjectives,
                animalColors,
                animalNouns,
                animalVerbs,
                natureAdjectives,
                natureNouns,
                plantNouns,
                plantVerbs
            ]
        return key

    @staticmethod
    def write_haiku(word_array, ipv6):
        octet = 'OCTET'  # String to place in schema to show word slots
        schema_results = Hipku.get_schema(ipv6, octet)
        schema = schema_results[0]
        non_words = schema_results[1]

        # Replace each instance of 'octet' in the schema with a word from the encoded word array
        word_index = 0
        for i in range(len(schema)):
            if schema[i] == octet:
                schema[i] = word_array[word_index]
                word_index += 1
                if word_index >= len(word_array):
                    break

        # Capitalize appropriate words
        schema = Hipku.capitalize_haiku(schema)
        haiku = ''.join(schema)

        return haiku

    @staticmethod
    def get_schema(ipv6, octet):
        schema = []
        new_line = '\n'
        period = '.'
        space = ' '
        non_words = [new_line, period, space]

        if ipv6:
            schema = [
                octet, octet, 'and', octet, octet, new_line,
                octet, octet, octet, octet, octet, octet, octet, period, new_line,
                octet, octet, octet, octet, octet, period, new_line
            ]
        else:
            schema = [
                'The', octet, octet, octet, new_line,
                octet, 'in the', octet, octet, period, new_line,
                octet, octet, period, new_line
            ]

        # Add spaces before words except the first word
        i = 1
        while i < len(schema):
            insert_space = True

            # If the next entry is a nonWord, don't add a space
            for non_word in non_words:
                if schema[i] == non_word:
                    insert_space = False
                    break

            # If the previous entry is a newLine, don't add a space
            if schema[i - 1] == new_line:
                insert_space = False

            if insert_space:
                schema.insert(i, space)
                i += 1
            i += 1

        return [schema, non_words]

    @staticmethod
    def capitalize_haiku(haiku_array):
        period = '.'

        # Always capitalize the first word
        if len(haiku_array) > 0:
            haiku_array[0] = Hipku.capitalize_word(haiku_array[0])

        for i in range(1, len(haiku_array)):
            if haiku_array[i] == period and i + 2 < len(haiku_array):
                # If the current entry is a period then the next entry will be
                # a newLine or a space, so check two positions ahead and
                # capitalize that entry, so long as it's a word
                haiku_array[i + 2] = Hipku.capitalize_word(haiku_array[i + 2])

        return haiku_array

    @staticmethod
    def capitalize_word(word):
        if len(word) == 0:
            return word
        return word[0].upper() + word[1:]

    # Helper functions for decoding
    @staticmethod
    def split_haiku(haiku):
        haiku = haiku.lower()

        # Replace newline characters with spaces
        haiku = re.sub(r'\n', ' ', haiku)

        # Remove anything that's not a letter, a space or a dash
        haiku = re.sub(r'[^a-z\ -]', '', haiku)
        word_array = haiku.split(' ')

        # Remove any blank entries
        word_array = [word for word in word_array if word != '']

        return word_array

    @staticmethod
    def haiku_is_ipv6(word_array):
        key = Hipku.get_key(False)
        dictionary = key[0]
        ipv6 = True

        # Compare each word in the haiku against each word in the first
        # dictionary defined in the IPv4 key. If there's a match, the
        # current haiku is IPv4. If not, IPv6.
        for current_word in word_array:
            if current_word in dictionary:
                ipv6 = False
                break

        return ipv6

    @staticmethod
    def get_factors(word_array, ipv6):
        key = Hipku.get_key(ipv6)
        factor_array = []
        word_array_position = 0

        # Get the first dictionary from the key. Check the first entry in
        # the encoded word array to see if it's in that dictionary. If it
        # is, store the dictionary offset and move onto the next dictionary
        # and the next word in the encoded words array. If there isn't a
        # match, keep the same dictionary but check the next word in the
        # array. Keep going till we have an offset for each dictionary in
        # the key.
        for dictionary in key:
            result = Hipku.get_factor_from_word(dictionary, len(key), word_array, word_array_position)
            factor = result[0]
            word_array_position = result[1]
            factor_array.append(factor)

        return factor_array

    @staticmethod
    def get_factor_from_word(dictionary, max_length, words, position):
        factor = None
        dict_entry_length = 0
        word_to_check = ''

        for j in range(len(dictionary)):
            # Get the number of words in the dictionary entry
            dict_entry_words = dictionary[j].split(' ')
            dict_entry_length = len(dict_entry_words)

            # build a string to compare against the dictionary entry
            # by joining the appropriate number of word_array entries
            if position + dict_entry_length > len(words):
                continue
                
            word_to_check = ' '.join(words[position:position + dict_entry_length])

            if dictionary[j] == word_to_check:
                factor = j
                # If the dictionary entry word count is greater than one,
                # increment the position counter by the difference to
                # avoid rechecking words we've already checked
                position += (dict_entry_length - 1)
                break

        position += 1

        if factor is None:
            if position >= max_length:
                # We've reached the entry of the haiku and still not matched
                # all necessary dictionaries, so throw an error
                raise ValueError('Decoding error: one or more dictionary words missing from input haiku')
            else:
                # Couldn't find the current word in the current dictionary,
                # try the next word
                return Hipku.get_factor_from_word(dictionary, max_length, words, position)
        else:
            # Found the word - return the dictionary offset and the new
            # word array position
            return [factor, position]

    @staticmethod
    def get_octets(factor_array, ipv6):
        octet_array = []
        if ipv6:
            multiplier = 256
        else:
            multiplier = 16

        for i in range(0, len(factor_array), 2):
            if i + 1 >= len(factor_array):
                break
            factor1 = factor_array[i]
            factor2 = factor_array[i + 1]
            octet = (factor1 * multiplier) + factor2

            if ipv6:
                octet = format(octet, 'x')

            octet_array.append(str(octet))

        return octet_array

    @staticmethod
    def get_ip_string(octet_array, ipv6):
        if ipv6:
            separator = ':'
        else:
            separator = '.'
        return separator.join(octet_array)




animalAdjectives = ['agile',
  'bashful',
  'clever',
  'clumsy',
  'drowsy',
  'fearful',
  'graceful',
  'hungry',
  'lonely',
  'morose',
  'placid',
  'ruthless',
  'silent',
  'thoughtful',
  'vapid',
  'weary']

animalColors = ['beige',
  'black',
  'blue',
  'bright',
  'bronze',
  'brown',
  'dark',
  'drab',
  'green',
  'gold',
  'grey',
  'jade',
  'pale',
  'pink',
  'red',
  'white']

animalNouns = ['ape',
  'bear',
  'crow',
  'dove',
  'frog',
  'goat',
  'hawk',
  'lamb',
  'mouse',
  'newt',
  'owl',
  'pig',
  'rat',
  'snake',
  'toad',
  'wolf']

animalVerbs = ['aches',
  'basks',
  'cries',
  'dives',
  'eats',
  'fights',
  'groans',
  'hunts',
  'jumps',
  'lies',
  'prowls',
  'runs',
  'sleeps',
  'thrives',
  'wakes',
  'yawns']

natureAdjectives = ['ancient',
  'barren',
  'blazing',
  'crowded',
  'distant',
  'empty',
  'foggy',
  'fragrant',
  'frozen',
  'moonlit',
  'peaceful',
  'quiet',
  'rugged',
  'serene',
  'sunlit',
  'wind-swept']

natureNouns = ['canyon',
  'clearing',
  'desert',
  'foothills',
  'forest',
  'grasslands',
  'jungle',
  'meadow',
  'mountains',
  'prairie',
  'river',
  'rockpool',
  'sand-dune',
  'tundra',
  'valley',
  'wetlands']

plantNouns = ['autumn colors',
  'cherry blossoms',
  'chrysanthemums',
  'crabapple blooms',
  'the dry palm fronds',
  'fat horse chestnuts',
  'forget-me-nots',
  'jasmine petals',
  'lotus flowers',
  'ripe blackberries',
  'the maple seeds',
  'the pine needles',
  'tiger lillies',
  'water lillies',
  'willow branches',
  'yellowwood leaves']

plantVerbs = ['blow',
  'crunch',
  'dance',
  'drift',
  'drop',
  'fall',
  'grow',
  'pile',
  'rest',
  'roll',
  'show',
  'spin',
  'stir',
  'sway',
  'turn',
  'twist']

adjectives = ['ace',
  'apt',
  'arched',
  'ash',
  'bad',
  'bare',
  'beige',
  'big',
  'black',
  'bland',
  'bleak',
  'blond',
  'blue',
  'blunt',
  'blush',
  'bold',
  'bone',
  'both',
  'bound',
  'brash',
  'brass',
  'brave',
  'brief',
  'brisk',
  'broad',
  'bronze',
  'brushed',
  'burned',
  'calm',
  'ceil',
  'chaste',
  'cheap',
  'chilled',
  'clean',
  'coarse',
  'cold',
  'cool',
  'corn',
  'crass',
  'crazed',
  'cream',
  'crisp',
  'crude',
  'cruel',
  'cursed',
  'cute',
  'daft',
  'damp',
  'dark',
  'dead',
  'deaf',
  'dear',
  'deep',
  'dense',
  'dim',
  'drab',
  'dry',
  'dull',
  'faint',
  'fair',
  'fake',
  'false',
  'famed',
  'far',
  'fast',
  'fat',
  'fierce',
  'fine',
  'firm',
  'flat',
  'flawed',
  'fond',
  'foul',
  'frail',
  'free',
  'fresh',
  'full',
  'fun',
  'glum',
  'good',
  'grave',
  'gray',
  'great',
  'green',
  'grey',
  'grim',
  'gruff',
  'hard',
  'harsh',
  'high',
  'hoarse',
  'hot',
  'huge',
  'hurt',
  'ill',
  'jade',
  'jet',
  'jinxed',
  'keen',
  'kind',
  'lame',
  'lank',
  'large',
  'last',
  'late',
  'lean',
  'lewd',
  'light',
  'limp',
  'live',
  'loath',
  'lone',
  'long',
  'loose',
  'lost',
  'louche',
  'loud',
  'low',
  'lush',
  'mad',
  'male',
  'masked',
  'mean',
  'meek',
  'mild',
  'mint',
  'moist',
  'mute',
  'near',
  'neat',
  'new',
  'nice',
  'nude',
  'numb',
  'odd',
  'old',
  'pained',
  'pale',
  'peach',
  'pear',
  'peeved',
  'pink',
  'piqued',
  'plain',
  'plum',
  'plump',
  'plush',
  'poor',
  'posed',
  'posh',
  'prim',
  'prime',
  'prompt',
  'prone',
  'proud',
  'prune',
  'puce',
  'pure',
  'quaint',
  'quartz',
  'quick',
  'rare',
  'raw',
  'real',
  'red',
  'rich',
  'ripe',
  'rough',
  'rude',
  'rushed',
  'rust',
  'sad',
  'safe',
  'sage',
  'sane',
  'scorched',
  'shaped',
  'sharp',
  'sheared',
  'short',
  'shrewd',
  'shrill',
  'shrunk',
  'shy',
  'sick',
  'skilled',
  'slain',
  'slick',
  'slight',
  'slim',
  'slow',
  'small',
  'smart',
  'smooth',
  'smug',
  'snide',
  'snug',
  'soft',
  'sore',
  'sought',
  'sour',
  'spare',
  'sparse',
  'spent',
  'spoilt',
  'spry',
  'squat',
  'staid',
  'stale',
  'stark',
  'staunch',
  'steep',
  'stiff',
  'strange',
  'straw',
  'stretched',
  'strict',
  'striped',
  'strong',
  'suave',
  'sure',
  'svelte',
  'swank',
  'sweet',
  'swift',
  'tall',
  'tame',
  'tan',
  'tart',
  'taut',
  'teal',
  'terse',
  'thick',
  'thin',
  'tight',
  'tiny',
  'tired',
  'toothed',
  'torn',
  'tough',
  'trim',
  'trussed',
  'twin',
  'used',
  'vague',
  'vain',
  'vast',
  'veiled',
  'vexed',
  'vile',
  'warm',
  'weak',
  'webbed',
  'wrong',
  'wry',
  'young']

nouns = ['ants',
  'apes',
  'asps',
  'balls',
  'barb',
  'barbs',
  'bass',
  'bats',
  'beads',
  'beaks',
  'bears',
  'bees',
  'bells',
  'belts',
  'birds',
  'blades',
  'blobs',
  'blooms',
  'boars',
  'boats',
  'bolts',
  'books',
  'bowls',
  'boys',
  'bream',
  'brides',
  'broods',
  'brooms',
  'brutes',
  'bucks',
  'bulbs',
  'bulls',
  'burls',
  'cakes',
  'calves',
  'capes',
  'cats',
  'char',
  'chests',
  'choirs',
  'clams',
  'clans',
  'clouds',
  'clowns',
  'cod',
  'coins',
  'colts',
  'cones',
  'cords',
  'cows',
  'crabs',
  'cranes',
  'crows',
  'cults',
  'czars',
  'darts',
  'dates',
  'deer',
  'dholes',
  'dice',
  'discs',
  'does',
  'dogs',
  'doors',
  'dopes',
  'doves',
  'drakes',
  'dreams',
  'drones',
  'ducks',
  'dunes',
  'eels',
  'eggs',
  'elk',
  'elks',
  'elms',
  'elves',
  'ewes',
  'eyes',
  'faces',
  'facts',
  'fawns',
  'feet',
  'ferns',
  'fish',
  'fists',
  'flames',
  'fleas',
  'flocks',
  'flutes',
  'foals',
  'foes',
  'fools',
  'fowl',
  'frogs',
  'fruits',
  'gangs',
  'gar',
  'geese',
  'gems',
  'germs',
  'ghosts',
  'gnomes',
  'goats',
  'grapes',
  'grooms',
  'grouse',
  'grubs',
  'guards',
  'gulls',
  'hands',
  'hares',
  'hawks',
  'heads',
  'hearts',
  'hens',
  'herbs',
  'hills',
  'hogs',
  'holes',
  'hordes',
  'ide',
  'jars',
  'jays',
  'kids',
  'kings',
  'kites',
  'lads',
  'lakes',
  'lambs',
  'larks',
  'lice',
  'lights',
  'limbs',
  'looms',
  'loons',
  'mares',
  'masks',
  'mice',
  'mimes',
  'minks',
  'mists',
  'mites',
  'mobs',
  'molds',
  'moles',
  'moons',
  'moths',
  'newts',
  'nymphs',
  'orbs',
  'orcs',
  'owls',
  'pearls',
  'pears',
  'peas',
  'perch',
  'pigs',
  'pikes',
  'pines',
  'plains',
  'plants',
  'plums',
  'pools',
  'prawns',
  'prunes',
  'pugs',
  'punks',
  'quail',
  'quails',
  'queens',
  'quills',
  'rafts',
  'rains',
  'rams',
  'rats',
  'rays',
  'ribs',
  'rocks',
  'rooks',
  'ruffs',
  'runes',
  'sands',
  'seals',
  'seas',
  'seeds',
  'serfs',
  'shards',
  'sharks',
  'sheep',
  'shells',
  'ships',
  'shoals',
  'shrews',
  'shrimp',
  'skate',
  'skies',
  'skunks',
  'sloths',
  'slugs',
  'smew',
  'smiles',
  'snails',
  'snakes',
  'snipes',
  'sole',
  'songs',
  'spades',
  'sprats',
  'sprouts',
  'squabs',
  'squads',
  'squares',
  'squid',
  'stars',
  'stoats',
  'stones',
  'storks',
  'strays',
  'suns',
  'swans',
  'swarms',
  'swells',
  'swifts',
  'tars',
  'teams',
  'teeth',
  'terns',
  'thorns',
  'threads',
  'thrones',
  'ticks',
  'toads',
  'tools',
  'trees',
  'tribes',
  'trolls',
  'trout',
  'tunes',
  'tusks',
  'veins',
  'verbs',
  'vines',
  'voles',
  'wasps',
  'waves',
  'wells',
  'whales',
  'whelks',
  'whiffs',
  'winds',
  'wolves',
  'worms',
  'wraiths',
  'wrens',
  'yaks']

verbs = ['aid',
  'arm',
  'awe',
  'axe',
  'bag',
  'bait',
  'bare',
  'bash',
  'bathe',
  'beat',
  'bid',
  'bilk',
  'blame',
  'bleach',
  'bleed',
  'bless',
  'bluff',
  'blur',
  'boast',
  'boost',
  'boot',
  'bore',
  'botch',
  'breed',
  'brew',
  'bribe',
  'brief',
  'brine',
  'broil',
  'browse',
  'bruise',
  'build',
  'burn',
  'burst',
  'call',
  'calm',
  'carve',
  'chafe',
  'chant',
  'charge',
  'chart',
  'cheat',
  'check',
  'cheer',
  'chill',
  'choke',
  'chomp',
  'choose',
  'churn',
  'cite',
  'clamp',
  'clap',
  'clasp',
  'claw',
  'clean',
  'cleanse',
  'clip',
  'cloak',
  'clone',
  'clutch',
  'coax',
  'crack',
  'crave',
  'crunch',
  'cry',
  'cull',
  'cure',
  'curse',
  'cuss',
  'dare',
  'daze',
  'dent',
  'dig',
  'ding',
  'doubt',
  'dowse',
  'drag',
  'drain',
  'drape',
  'draw',
  'dread',
  'dredge',
  'drill',
  'drink',
  'drip',
  'drive',
  'drop',
  'drown',
  'dry',
  'dump',
  'eat',
  'etch',
  'face',
  'fail',
  'fault',
  'fear',
  'feed',
  'feel',
  'fetch',
  'fight',
  'find',
  'fix',
  'flap',
  'flay',
  'flee',
  'fling',
  'flip',
  'float',
  'foil',
  'forge',
  'free',
  'freeze',
  'frisk',
  'gain',
  'glimpse',
  'gnaw',
  'goad',
  'gouge',
  'grab',
  'grasp',
  'graze',
  'grieve',
  'grip',
  'groom',
  'guard',
  'guards',
  'guide',
  'gulp',
  'gush',
  'halt',
  'harm',
  'hate',
  'haul',
  'haunt',
  'have',
  'heal',
  'hear',
  'help',
  'herd',
  'hex',
  'hire',
  'hit',
  'hoist',
  'hound',
  'hug',
  'hurl',
  'irk',
  'jab',
  'jeer',
  'join',
  'jolt',
  'keep',
  'kick',
  'kill',
  'kiss',
  'lash',
  'leash',
  'leave',
  'lift',
  'like',
  'love',
  'lug',
  'lure',
  'maim',
  'make',
  'mask',
  'meet',
  'melt',
  'mend',
  'miss',
  'mould',
  'move',
  'nab',
  'name',
  'need',
  'oust',
  'paint',
  'paw',
  'pay',
  'peck',
  'peeve',
  'pelt',
  'please',
  'pluck',
  'poach',
  'poll',
  'praise',
  'prick',
  'print',
  'probe',
  'prod',
  'prompt',
  'punch',
  'quash',
  'quell',
  'quote',
  'raid',
  'raise',
  'raze',
  'ride',
  'roast',
  'rouse',
  'rule',
  'scald',
  'scalp',
  'scar',
  'scathe',
  'score',
  'scorn',
  'scour',
  'scuff',
  'sear',
  'see',
  'seek',
  'seize',
  'send',
  'sense',
  'serve',
  'shake',
  'shear',
  'shift',
  'shoot',
  'shun',
  'slap',
  'slay',
  'slice',
  'smack',
  'smash',
  'smell',
  'smite',
  'snare',
  'snatch',
  'sniff',
  'snub',
  'soak',
  'spare',
  'splash',
  'split',
  'spook',
  'spray',
  'squash',
  'squeeze',
  'stab',
  'stain',
  'starve',
  'steal',
  'steer',
  'sting',
  'strike',
  'stun',
  'tag',
  'tame',
  'taste',
  'taunt',
  'teach',
  'tend']

