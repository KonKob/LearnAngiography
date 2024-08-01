import pandas as pd

segment_definitions_dict = {'segment_id': {0: '1',
  1: '2',
  2: '3',
  3: '4',
  4: '5',
  5: '6',
  6: '7',
  7: '8',
  8: '9',
  9: '10',
  10: '11',
  11: '12',
  12: '13',
  13: '14',
  14: '15',
  15: '24',
  16: '16',
  17: '17',
  18: '18',
  19: '25',
  20: '19',
  21: '20',
  22: '21',
  23: '22',
  24: '23',
  25: '26'},
 'segment_alphanumeric': {0: '1',
  1: '2',
  2: '3',
  3: '4',
  4: '5',
  5: '6',
  6: '7',
  7: '8',
  8: '9',
  9: '9a',
  10: '10',
  11: '10a',
  12: '11',
  13: '12',
  14: '12a',
  15: '12b',
  16: '13',
  17: '14',
  18: '14a',
  19: '14b',
  20: '15',
  21: '16',
  22: '16a',
  23: '16b',
  24: '16c',
  25: 'stenosis'},
 'segment_name': {0: 'RCA proximal',
  1: 'RCA mid',
  2: 'RCA distal ',
  3: 'Posterior descending',
  4: 'Left main',
  5: 'LAD proximal',
  6: 'LAD mid',
  7: 'LAD apical',
  8: 'First diagonal',
  9: 'First diagonal a',
  10: 'Second diagonal',
  11: 'Second diagonal a',
  12: 'Proximal circumflex',
  13: 'Intermediate/anterolateral',
  14: 'Obtuse marginal a',
  15: 'Obtuse marginal b',
  16: 'Distal circumflex',
  17: 'Left posterolateral',
  18: 'Left posterolateral a',
  19: 'Left posterolateral b',
  20: 'Posterior descending',
  21: 'Posterolateral from RCA',
  22: 'Posterolateral from RCA',
  23: 'Posterolateral from RCA',
  24: 'Posterolateral from RCA',
  25: 'stenosis'},
 'segment_description': {0: 'From ostium to one half the distance to the acute margin of the heart.',
  1: 'From end of first segment to acute margin of heart.',
  2: 'From the acute margin of the heart to the origin of the posterior descending artery.',
  3: 'Running in the posterior interventricular groove.',
  4: 'From the ostium of the LCA through bifurcation into left anterior descending and left circumflex branches.',
  5: 'Proximal to and including first major septal branch.',
  6: 'LAD immediately distal to origin of first septal branch and extending to the point where LAD forms an angle (RAO view). If this angle is not identifiable this segment ends at one half the distance from the first septal to the apex of the heart.',
  7: 'Terminal portion of LAD; beginning at the end of previous segment and extending to or beyond the apex.',
  8: 'The first diagonal originating from segment 6 or 7.',
  9: 'Additional first diagonal originating from segment 6 or 7; before segment 8.',
  10: 'Second diagonal originating from segment 8 or the transition between segment 7 and 8.',
  11: 'Additional second diagonal originating from segment 8.',
  12: 'Main stem of circumflex from its origin of left main to and including origin of first obtuse marginal branch.',
  13: 'Branch from trifurcating left main other than proximal LAD or LCX. Belongs to the circumflex territory. ',
  14: 'First side branch of circumflex running in general to the area of obtuse margin of the heart.',
  15: 'Second additional branch of circumflex running in the same direction as 12.',
  16: 'The stem of the circumflex distal to the origin of the most distal obtuse marginal branch and running along the posterior left atrioventricular grooves. Caliber may be small or artery absent.',
  17: 'Running to the posterolateral surface of the left ventricle. May be absent or a division of obtuse marginal branch.',
  18: 'Distal from 14 and running in the same direction.',
  19: 'Distal from 14 and 14 a and running in the same direction.',
  20: 'Most distal part of dominant left circumflex when present. Gives origin to septal branches. When this artery is present; segment 4 is usually absent.',
  21: 'Posterolateral branch originating from the distal coronary artery distal to the crux.',
  22: 'First posterolateral branch from segment 16.',
  23: 'Second posterolateral branch from segment 16.',
  24: 'Third posterolateral branch from segment 16.',
  25: 'stenosis'}}

segment_definitions = pd.DataFrame(segment_definitions_dict)


segment_definitions_markdown = """      

        ## The module questions rely on the definitions taken from syntax score.
        [https://syntaxscore.org/index.php/tutorial/definitions](https://syntaxscore.org/index.php/tutorial/definitions)

        |syntax score|name|description|
        |:---|:---|:---|
        | RCA proximal | From ostium to one half the distance to the acute margin of the heart. |
        | 2 | RCA mid | From end of first segment to acute margin of heart. |
        | 3 | RCA distal | From the acute margin of the heart to the origin of the posterior descending artery. |
        | 4 | Posterior descending | Running in the posterior interventricular groove. |
        | 5 | Left main | From the ostium of the LCA through bifurcation into left anterior descending and left circumflex branches. |
        | 6 | LAD proximal | Proximal to and including first major septal branch. |
        | 7 | LAD mid | LAD immediately distal to origin of first septal branch and extending to the point where LAD forms an angle (RAO view). If this angle is not identifiable this segment ends at one half the distance from the first septal to the apex of the heart. |
        | 8 | LAD apical | Terminal portion of LAD; beginning at the end of previous segment and extending to or beyond the apex. |
        | 9 | First diagonal | The first diagonal originating from segment 6 or 7. |
        | 9a | First diagonal a | Additional first diagonal originating from segment 6 or 7; before segment 8. |
        | 10 | Second diagonal | Second diagonal originating from segment 8 or the transition between segment 7 and 8. |
        | 10a | Second diagonal a | Additional second diagonal originating from segment 8. |
        | 11 | Proximal circumflex | Main stem of circumflex from its origin of left main to and including origin of first obtuse marginal branch. |
        | 12 | Intermediate/anterolateral | Branch from trifurcating left main other than proximal LAD or LCX. Belongs to the circumflex territory. |
        | 12a | Obtuse marginal a | First side branch of circumflex running in general to the area of obtuse margin of the heart. |
        | 12b | Obtuse marginal b | Second additional branch of circumflex running in the same direction as 12. |
        | 13 | Distal circumflex | The stem of the circumflex distal to the origin of the most distal obtuse marginal branch and running along the posterior left atrioventricular grooves. Caliber may be small or artery absent. |
        | 14 | Left posterolateral | Running to the posterolateral surface of the left ventricle. May be absent or a division of obtuse marginal branch. |
        | 14a | Left posterolateral a | Distal from 14 and running in the same direction. |
        | 14b | Left posterolateral b | Distal from 14 and 14 a and running in the same direction. |
        | 15 | Posterior descending | Most distal part of dominant left circumflex when present. Gives origin to septal branches. When this artery is present; segment 4 is usually absent. |
        | 16 | Posterolateral from RCA | Posterolateral branch originating from the distal coronary artery distal to the crux. |
        | 16a | Posterolateral from RCA | First posterolateral branch from segment 16. |
        | 16b | Posterolateral from RCA | Second posterolateral branch from segment 16. |
        | 16c | Posterolateral from RCA | Third posterolateral branch from segment 16. |
        """