piece_coords = {'o': {1: [[3, 3], [4, 3], [3, 4], [4, 4]] },
                'i': {1: [[2, 2], [3, 2], [4, 2], [5, 2]], 2: [[4, 2], [4, 3], [4, 4], [4, 5]] },
                's': {1: [[4, 2], [4, 3], [5, 3], [5, 4]], 2: [[4, 4], [5, 4], [3, 5], [4, 5]] },
                'z': {1: [[4, 2], [3, 3], [4, 3], [3, 4]], 2: [[3, 4], [4, 4], [4, 5], [5, 5]] },
                'l': {1: [[4, 2], [4, 3], [4, 4], [5, 4]],
                      2: [[3, 3], [4, 3], [5, 3], [3, 4]],
                      3: [[3, 3], [4, 3], [4, 4], [4, 5]],
                      4: [[5, 5], [3, 6], [4, 6], [5, 6]] },
                't': {1: [[4, 2], [4, 3], [5, 3], [4, 4]],
                      2: [[3, 4], [4, 4], [5, 4], [4, 5]],
                      3: [[4, 2], [3, 3], [4, 3], [4, 4]],
                      4: [[4, 3], [3, 4], [4, 4], [5, 4]]},
                'j': {1: [[4, 2], [5, 2], [4, 3], [4, 4]],
                      2: [[3, 4], [4, 4], [5, 4], [5, 5]], 
                      3: [[4, 4], [4, 5], [3, 6], [4, 6]],
                      4: [[3, 5], [3, 6], [4, 6], [5, 6]]},
                }

# returns the piece type (o, j, l , s, z, t, i)) 
def recon_piece(piece):
    piece_type = None
    
    if piece[0][0] == piece[1][0]-1 == piece[2][0] == piece[3][0]-1 and piece[0][1] == piece[1][1] == piece[2][1]-1 == piece[3][1]-1:
        piece_type = 'o'
    else:
        if piece[0][0] == piece[1][0] == piece[2][0]-1 == piece[3][0]-1 and piece[0][1]+1 == piece[1][1] == piece[2][1] == piece[3][1]-1 \
            or piece[0][0] == piece[1][0]-1 == piece[2][0]+1 == piece[3][0] and piece[0][1] == piece[1][1] == piece[2][1]-1 == piece[3][1]-1:
            piece_type = 's' 
        else:
            if piece[0][0]-1 == piece[1][0] == piece[2][0]-1 == piece[3][0] and piece[0][1] == piece[1][1]-1 == piece[2][1]-1 == piece[3][1]-2 \
                or piece[0][0] == piece[1][0]-1 == piece[2][0]-1 == piece[3][0]-2 and piece[0][1] == piece[1][1] == piece[2][1]-1 == piece[3][1]-1:
                piece_type = 'z'
            else:
                if piece[0][1] == piece[1][1] == piece[2][1] == piece[3][1] \
                    or piece[0][0] == piece[1][0] == piece[2][0] == piece[3][0]:
                    piece_type = 'i'
                else:
                    if piece[0][0] == piece[1][0] == piece[2][0] and piece[0][1] == piece[1][1]-1 == piece[2][1]-2 == piece[3][1]-2 \
                        or piece[0][0] == piece[1][0]-1 == piece[2][0]-2 == piece[3][0] and piece[0][1] == piece[1][1] == piece[2][1] == piece[3][1]-1 \
                        or piece[0][0] == piece[1][0]-1 == piece[2][0]-1 == piece[3][0]-1 and piece[0][1] == piece[1][1] == piece[2][1]-1 == piece[3][1]-2 \
                        or piece[0][0] == piece[1][0]+2 == piece[2][0]+1 == piece[3][0] and piece[0][1] == piece[1][1]-1 == piece[2][1]-1 == piece[3][1]-1:
                        piece_type = 'l'
                    else:
                        if piece[0][0] == piece[1][0] == piece[2][0]-1 == piece[3][0] and piece[0][1]+1 == piece[1][1] == piece[2][1] == piece[3][1]-1 \
                            or piece[0][0] == piece[1][0]-1 == piece[2][0]-2 == piece[3][0]-1 and piece[0][1] == piece[1][1] == piece[2][1] == piece[3][1]-1 \
                            or piece[0][0] == piece[1][0]+1 == piece[2][0] == piece[3][0] and piece[0][1] == piece[1][1]-1 == piece[2][1]-1 == piece[3][1]-2 \
                            or piece[0][0] == piece[1][0]+1 == piece[2][0] == piece[3][0]-1 and piece[0][1] == piece[1][1]-1 == piece[2][1]-1 == piece[3][1]-1:
                            piece_type = 't'
                        else:
                            if piece[0][0] == piece[1][0]-1 == piece[2][0] == piece[3][0] and piece[0][1] == piece[1][1] == piece[2][1]-1 == piece[3][1]-2 \
                                or piece[0][0] == piece[1][0]-1 == piece[2][0]-2 == piece[3][0]-2 and piece[0][1] == piece[1][1] == piece[2][1] == piece[3][1]-1 \
                                or piece[0][0] == piece[1][0] == piece[2][0]+1 == piece[3][0] and piece[0][1] == piece[1][1]-1 == piece[2][1]-2 == piece[3][1]-2 \
                                or piece[0][0] == piece[1][0] == piece[2][0]-1 == piece[3][0]-2 and piece[0][1] == piece[1][1]-1 == piece[2][1]-1 == piece[3][1]-1:
                                piece_type = 'j'
    
    return piece_type

def get_height(piece):
    return max(row[1] for row in piece)

def main():
        
    p = piece_coords['o'][1]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['i'][1]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['i'][2]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['s'][1]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['s'][2]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['z'][1]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['z'][2]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['l'][1]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['l'][2]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['l'][3]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['l'][4]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['t'][1]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['t'][2]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['t'][3]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['t'][4]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['j'][1]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['j'][2]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['j'][3]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

    p = piece_coords['j'][4]
    p_type = recon_piece(p)
    print(p_type)
    print(get_height(p))
    print("\n")

if __name__ == '__main__':
    main()
    