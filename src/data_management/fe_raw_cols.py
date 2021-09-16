from colassigner import ColAccessor


class Sides(ColAccessor):
    home = "home"
    away = "away"


class CommonCols(ColAccessor):
    _prefix = "fe"

    season_id = "season_id"
    match_id = "match_id"
    event_id = "event_id"
    player_id = "player_id"
    team_id = "team_id"
    formation_id = "formation_id"

    area_name = "area_name"


class EventsCols(ColAccessor):
    period = "period"
    event_type = "event_type"
    outcometype = "outcometype"
    event_side = "event_side"
    zone = "zone"
    local_event_id = "local_event_id"
    minute = "minute"
    second = "second"
    x = "x"
    y = "y"

    class Related(ColAccessor):
        _prefix = "related"
        event = CommonCols.event_id
        player = CommonCols.player_id

    expandedminute = "expandedminute"
    istouch = "istouch"
    length = "length"
    angle = "angle"
    passendx = "passendx"
    passendy = "passendy"
    chipped = "chipped"
    longball = "longball"
    oppositerelatedevent = "oppositerelatedevent"
    offensive = "offensive"
    defensive = "defensive"
    missleft = "missleft"
    missright = "missright"
    cross = "cross"
    cornertaken = "cornertaken"
    misshigh = "misshigh"
    goalkick = "goalkick"
    headpass = "headpass"
    head = "head"
    throwin = "throwin"
    foul = "foul"
    goalmouthz = "goalmouthz"
    goalmouthy = "goalmouthy"
    isshot = "isshot"
    outofboxcentre = "outofboxcentre"
    highleft = "highleft"
    leftfoot = "leftfoot"
    directfreekick = "directfreekick"
    playercaughtoffside = "playercaughtoffside"
    freekicktaken = "freekicktaken"
    indirectfreekicktaken = "indirectfreekicktaken"
    blockedcross = "blockedcross"
    throughball = "throughball"
    intentionalassist = "intentionalassist"
    shotassist = "shotassist"
    keypass = "keypass"
    fromcorner = "fromcorner"
    assisted = "assisted"
    boxcentre = "boxcentre"
    regularplay = "regularplay"
    outofboxleft = "outofboxleft"
    yellow = "yellow"
    blockedx = "blockedx"
    blockedy = "blockedy"
    outofboxdeepright = "outofboxdeepright"
    blocked = "blocked"
    outfielderblock = "outfielderblock"
    leadingtoattempt = "leadingtoattempt"
    intentionalgoalassist = "intentionalgoalassist"
    isgoal = "isgoal"
    boxright = "boxright"
    rightfoot = "rightfoot"
    keeperthrow = "keeperthrow"
    layoff = "layoff"
    overrun = "overrun"
    highright = "highright"
    deepboxright = "deepboxright"
    lowright = "lowright"
    hands = "hands"
    parriedsafe = "parriedsafe"
    standingsave = "standingsave"
    keepersaveinthebox = "keepersaveinthebox"
    formationslot = "formationslot"
    penalty = "penalty"
    keepermissed = "keepermissed"
    divingsave = "divingsave"
    lowleft = "lowleft"
    bigchance = "bigchance"
    boxleft = "boxleft"
    thirtyfivepluscentre = "thirtyfivepluscentre"
    bigchancecreated = "bigchancecreated"
    smallboxleft = "smallboxleft"
    sixyardblock = "sixyardblock"
    setpiece = "setpiece"
    goaldisallowed = "goaldisallowed"
    captainplayerid = "captainplayerid"
    teamformation = "teamformation"
    keepersaveobox = "keepersaveobox"
    highclaim = "highclaim"
    lowcentre = "lowcentre"
    aerialfoul = "aerialfoul"
    parrieddanger = "parrieddanger"
    collected = "collected"
    smallboxcentre = "smallboxcentre"
    deepboxleft = "deepboxleft"
    otherbodypart = "otherbodypart"
    throwinsetpiece = "throwinsetpiece"
    lastman = "lastman"
    outofboxdeepleft = "outofboxdeepleft"
    voidyellowcard = "voidyellowcard"
    feet = "feet"
    secondyellow = "secondyellow"
    obstruction = "obstruction"
    highcentre = "highcentre"
    outofboxright = "outofboxright"
    leadingtogoal = "leadingtogoal"
    fastbreak = "fastbreak"
    isowngoal = "isowngoal"
    owngoal = "owngoal"
    smallboxright = "smallboxright"
    red = "red"
    keepersaveinsixyard = "keepersaveinsixyard"
    thirtyfiveplusright = "thirtyfiveplusright"
    fromshotofftarget = "fromshotofftarget"
    keepersaved = "keepersaved"
    penaltyshootoutconcededgk = "penaltyshootoutconcededgk"
    keeperwentwide = "keeperwentwide"
    savedoffline = "savedoffline"
    thirtyfiveplusleft = "thirtyfiveplusleft"


class FormationsCols(ColAccessor):
    class Slot(ColAccessor):
        _prefix = "slot"

        class N1(ColAccessor):
            _prefix = "1"
            vertical = "vertical"
            horizontal = "horizontal"

        class N2(N1):
            _prefix = "2"

        class N3(N1):
            _prefix = "3"

        class N4(N1):
            _prefix = "4"

        class N5(N1):
            _prefix = "5"

        class N6(N1):
            _prefix = "6"

        class N7(N1):
            _prefix = "7"

        class N8(N1):
            _prefix = "8"

        class N9(N1):
            _prefix = "9"

        class N10(N1):
            _prefix = "10"

        class N11(N1):
            _prefix = "11"


class FormationUseCols(ColAccessor):
    captain = "captain"
    period = "period"
    side = "side"

    class Minute(ColAccessor):
        _prefix = "minute"
        start = "start"
        end = "end"

    class Slot(ColAccessor):
        _prefix = "slot"
        n1 = "n1"
        n2 = "n2"
        n3 = "n3"
        n4 = "n4"
        n5 = "n5"
        n6 = "n6"
        n7 = "n7"
        n8 = "n8"
        n9 = "n9"
        n10 = "n10"
        n11 = "n11"


class LineupsCols(ColAccessor):
    position = "position"
    shirt_no = "shirt_no"
    side = "side"
    age = "age"


class MatchesCols(ColAccessor):
    class Goals(ColAccessor):
        _prefix = "goals"

        class Home(ColAccessor):
            _prefix = "home"
            ht = "ht"
            ft = "ft"
            et = "et"
            pk = "pk"

        class Away(Home):
            _prefix = "away"

    class TeamId(Sides):
        _prefix = CommonCols.team_id

    class ManagerName(Sides):
        _prefix = "managername"

    class Progress(Sides):
        _prefix = "progress"

    score = "score"
    attendance = "attendance"
    venuename = "venuename"
    weathercode = "weathercode"
    referee_officialid = "referee_officialid"
    datetime = "datetime"


class PlayersCols(ColAccessor):
    name = "name"
    height = "height"


class SeasonsCols(ColAccessor):
    competition_name = "competition_name"
    season_year_name = "season_year_name"


class TeamsCols(ColAccessor):
    team_name = "team_name"
